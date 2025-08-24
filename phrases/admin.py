from django.contrib import admin, messages
from django.conf import settings

from .models import MedicalConcept, TermVariant, UnmappedTerm, MedicalSubject

import requests
import json

class MedicalConceptInline(admin.TabularInline):
    model= MedicalConcept.subject.through
    extra=1
    show_change_link = True
@admin.register(MedicalSubject)
class MedicalSubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_count']
    inlines=[MedicalConceptInline]
    def get_count(self, obj):
        return MedicalConcept.objects.filter(subject=obj).count()
    get_count.short_description = 'Number of Concepts'

@admin.register(TermVariant)
class TermVariantAdmin(admin.ModelAdmin):
    list_display = ['get_text', 'get_concept']
    search_fields = ['text']

    def get_concept(self, obj):
        return obj.concept.name
    def get_text(self, obj):
        return obj.text
    get_concept.short_description = "Concept"

class TermVariantInline(admin.TabularInline):   # or admin.StackedInline
    model = TermVariant
    extra = 1   # how many empty rows to show by default
    # fields = ["text", 'term_type']
    fields = ["text"]
    show_change_link = True


@admin.register(MedicalConcept)
class MedicalConceptAdmin(admin.ModelAdmin):
    list_display = ["name", "get_subject", "code"]
    search_fields = ["name", "get_subject", "code"]
    actions = ["generate_variants_action"]
    inlines = [TermVariantInline]
    
    def get_subject(self, obj):
        return ", ".join(c.name for c in obj.subject.all())
        
    def generate_variants_action(self, request, queryset):
        API_URL='https://api.metisai.ir/api/v1'
        for concept in queryset:
            if concept.ai_used == False:
                try:
                    bot_id = '4e8a5b03-1ad7-4db4-a5e1-5c2ba38fdc16'
                    bot_data={
                        'botId': bot_id,
                        'user':None,
                        'initialMessages': None,
                    }
                    Headers={
                    'Authorization':settings.AI_API_KEY,
                    'content-type':'application/json'
                    }
                    response=requests.post(API_URL+"/chat/session", headers=Headers, data=json.dumps(bot_data))
                    session_JSON = response.json()
                    session_ID=session_JSON.get('id')
                    print(session_ID)
                    # SESSION_CODE='47f9a62c-932a-4ec7-a60d-126485bb8220'
                    Headers={
                    'Authorization':settings.AI_API_KEY,
                    'content-type':'application/json'
                    }
                    Data = {
                        'message':{
                            'content': f"Medical Concept: {concept.name}",
                            'type':'USER'
                        },
                        }
                    message_url = f'{API_URL}/chat/session/{session_ID}/message'
                    response = requests.post(message_url, headers=Headers, data=json.dumps(Data))
                    response.raise_for_status()
                    variants = json.loads(response['content'])['variants']
                    print('List: ', variants)
                    for text in variants:
                    # for text in response['variants']:
                        TermVariant.objects.get_or_create(
                            text=text.lower().strip(),
                            defaults={
                                'concept':concept,
                            }
                        )
                    self.message_user(request, f"Variants Added for {concept.name} Successfully.")
                    
                except Exception as e:
                    self.message_user(request, f"Error calling AI API: {e}")
                queryset.update(ai_used=True)
            else:
                messages.error(request, f'Error: AI Variant Generator has already been used for {concept.name}.')
                
    get_subject.short_description = "Subjects"
    generate_variants_action.short_description = "Generate Variants with AI!"
    

@admin.register(UnmappedTerm)
class UnmappedTermAdmin(admin.ModelAdmin):
    list_display = ['text', 'concept','common_similarity', 'first_seen', 'last_seen', 'seen_count']
    search_fields = ['text']
    actions = ['assign_to_concept']

    def assign_to_concept(self, request, queryset):
        # You can replace this with a form in future for better UX
        for term in queryset:
            if term.concept:
                TermVariant.objects.create(text=term.text, concept=term.concept)
                term.delete()

        self.message_user(request, "Selected terms assigned to their concepts.")

    assign_to_concept.short_description = "Assign to its concept"






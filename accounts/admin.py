from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

@admin.action(description="Permit to Use CC AI")
def permit_CC_AI(CustomUser, request, queryset):
    queryset.update(hx_cc_ai_permission=True)

@admin.action(description="Forbid to Use CC AI")
def forbid_CC_AI(CustomUser, request, queryset):
    queryset.update(hx_cc_ai_permission=False)

@admin.action(description="Permit to Use PI AI")
def permit_PI_AI(CustomUser, request, queryset):
    queryset.update(hx_pi_ai_permission=True)

@admin.action(description="Permit to Use PhE AI")
def permit_PhE_AI(CustomUser, request, queryset):
    queryset.update(hx_phe_ai_permission=True)

@admin.action(description="Forbid to Use PI AI")
def forbid_PI_AI(CustomUser, request, queryset):
    queryset.update(hx_pi_ai_permission=False)

@admin.action(description="Permit to Use ROS AI")
def permit_ROS_AI(CustomUser, request, queryset):
    queryset.update(hx_ros_ai_permission=True)

@admin.action(description="Forbid to Use ROS AI")
def forbid_ROS_AI(CustomUser, request, queryset):
    queryset.update(hx_ros_ai_permission=False)


@admin.action(description="Forbid to Use PhE AI")
def forbid_PhE_AI(CustomUser, request, queryset):
    queryset.update(hx_phe_ai_permission=False)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    actions=[permit_CC_AI, permit_PI_AI, permit_ROS_AI, permit_PhE_AI, forbid_CC_AI, forbid_PI_AI, forbid_ROS_AI, forbid_PhE_AI]

    list_display = [
        "username",
        "first_name",
        "last_name",
        "degree",
        "university",
        "hx_cc_ai_permission",
        "hx_pi_ai_permission",
        "hx_ros_ai_permission",
        "hx_phe_ai_permission",
        "is_staff",
        "join_date_day",
        
    ]
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "field",
                    "university",
                    "degree",
                    "fn_fa",
                    "ln_fa",
                    "is_article_author",
                    "is_article_editor",
                    "is_case_editor",
                    "about_me",
                    "en_name",

                    "hx_cc_ai_permission",
                    "hx_cc_ai_use_count",

                    "hx_pi_ai_permission",
                    "hx_pi_ai_use_count",
                    
                    "hx_ros_ai_permission",
                    "hx_ros_ai_use_count",
                    
                    "hx_phe_ai_permission",
                    "hx_phe_ai_use_count",
                )
            },
        ),
    )

    list_display_links = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)


def generate_mappings(config_key, config_value, other_reference_mappings):
    return {
        "COGNITO_USER_POOL_NAME": config_key,
        "COGNITO_USER_POOL_DOMAIN_NAME": config_value["domain_name"],
        "COGNITO_ALLOW_ADMIN_CREATE_USER_ONLY": str(
            config_value.get("allow_admin_create_user_only", False)
        ).upper(),
        "COGNITO_ALIAS_ATTRIBUTE": config_value["alias_attributes"],
        "COGNITO_AUTO_VERIFIED_ATTRIBUTES": config_value["auto_verified_attributes"],
        "COGNITO_DELETION_PROTECTION": str(
            config_value.get("deletion_protection", False)
        ).upper(),
        "COGNITO_DEVICE_CONFIGURATION": {
            "challenge_required_on_new_device": str(
                config_value.get("device_configuration", {}).get(
                    "challenge_required_on_new_device", False
                )
            ).upper(),
            "device_only_remembered_on_user_prompt": str(
                config_value.get("device_configuration", {}).get(
                    "device_only_remembered_on_user_prompt", False
                )
            ).upper(),
        },
        "COGNITO_MFA_CONFIGURATION": config_value.get("mfa_configuration", "OPTIONAL"),
        "COGNITO_SOFTWARE_TOKEN_MFA_ENABLE": str(
            config_value.get("software_token_mfa_configuration_is_enabled", False)
        ).upper(),
        "COGNITO_PASSWORD_POLICY": {
            "minimum_length": config_value.get("password_policy", {}).get(
                "minimum_length", 12
            ),
            "require_lowercase": str(
                config_value.get("password_policy", {}).get("require_lowercase", True)
            ).upper(),
            "require_numbers": str(
                config_value.get("password_policy", {}).get("require_numbers", True)
            ).upper(),
            "require_symbols": str(
                config_value.get("password_policy", {}).get("require_symbols", True)
            ).upper(),
            "require_uppercase": str(
                config_value.get("password_policy", {}).get("require_uppercase", True)
            ).upper(),
            "temporary_password_validity_days": config_value.get(
                "password_policy", {}
            ).get("temporary_password_validity_days", 3),
        },
        "COGNITO_CLIENTS": [
            {
                "name": key,
                "access_token_validity": value.get("access_token_validity", 60),
                "id_token_validity": value.get("id_token_validity", 60),
                "refresh_token_validity": value.get("refresh_token_validity", 30),
            }
            for key, value in config_value.get("clients", {}).items()
        ],
    }

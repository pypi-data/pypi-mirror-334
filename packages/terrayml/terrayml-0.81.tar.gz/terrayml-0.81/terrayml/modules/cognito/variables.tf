variable "common" {
  description = "common variables"
}

variable "cognito_user_pool_list" {
  type = list(object({
    name = string
    domain_name = string
    allow_admin_create_user_only = string
    alias_attributes = list(string)
    auto_verified_attributes = list(string)
    deletion_protection = string
    device_configuration = object({
      challenge_required_on_new_device = string
      device_only_remembered_on_user_prompt = string
    })
    mfa_configuration = string
    software_token_mfa_configuration_is_enabled = string
    password_policy = object({
      minimum_length = number
      require_lowercase = string
      require_numbers = string
      require_symbols = string
      require_uppercase = string
      temporary_password_validity_days = number
    })
    clients = list(object({
      name = string
      access_token_validity = number
      id_token_validity = number
      refresh_token_validity = number
    }))
  }))
  description = "Cognito User Pool"
}

variable "cognito_identity_pool_list" {
  type = list(object({
    name = string
    allow_unauthenticated_identities = string
    cognito_identity_providers_list = list(object({
      user_pool_name = string
      client_name = string
      server_side_token_check = string
    }))
  }))
  description = "Cognito Identity Pool"
}

variable "cognito_lambda_trigger_list" {
  type = list(object({
    user_pool_id = string
    trigger_type = string
    lambda_function_arn = string
  }))
}
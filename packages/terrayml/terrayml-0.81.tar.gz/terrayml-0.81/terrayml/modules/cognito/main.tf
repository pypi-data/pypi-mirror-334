locals {
  cognito_clients = flatten([
    for user_pool_key, user_pool in var.cognito_user_pool_list: [
      for client_key, client in user_pool.clients: {
        user_pool_key = user_pool_key
        user_pool_name = user_pool.name
        client_key = client_key
        client_name = client.name
        user_pool_id = aws_cognito_user_pool.this[user_pool.name].id
        domain_name = user_pool.domain_name
        access_token_validity  = client.access_token_validity
        id_token_validity      = client.id_token_validity
        refresh_token_validity = client.refresh_token_validity
      }
    ]
  ])
}

resource "aws_cognito_user_pool" "this" {
  for_each      = { for key, value in var.cognito_user_pool_list : value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  admin_create_user_config {
    allow_admin_create_user_only = each.value.allow_admin_create_user_only == "TRUE" ? true : false
  }
  alias_attributes         = each.value.alias_attributes
  auto_verified_attributes = each.value.auto_verified_attributes
  deletion_protection      = each.value.deletion_protection == "TRUE"? "ACTIVE" : "INACTIVE"
  device_configuration {
    challenge_required_on_new_device      = each.value.device_configuration.challenge_required_on_new_device == "TRUE" ? true : false
    device_only_remembered_on_user_prompt = each.value.device_configuration.device_only_remembered_on_user_prompt == "TRUE" ? true : false
  }
  mfa_configuration = each.value.mfa_configuration
  software_token_mfa_configuration {
    enabled = each.value.software_token_mfa_configuration_is_enabled == "TRUE" ? true : false
  }
  password_policy {
    minimum_length                   = each.value.password_policy.minimum_length
    require_lowercase                = each.value.password_policy.require_lowercase == "TRUE" ? true : false
    require_numbers                  = each.value.password_policy.require_numbers == "TRUE" ? true: false
    require_symbols                  = each.value.password_policy.require_symbols == "TRUE" ? true : false
    require_uppercase                = each.value.password_policy.require_uppercase == "TRUE" ? true : false
    temporary_password_validity_days = each.value.password_policy.temporary_password_validity_days
  }
  tags = var.common.default_tags 
   
  lifecycle {
    ignore_changes = [
      lambda_config
    ]
  }

}

resource "aws_cognito_user_pool_client" "this" {
  for_each = tomap({
    for client in local.cognito_clients: "${client.user_pool_name}.${client.client_name}" => client
  })
  name         = "${var.common.project_code}-${var.common.environment}-${each.value.client_name}"
  user_pool_id = each.value.user_pool_id
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }

  access_token_validity  = each.value.access_token_validity
  id_token_validity      = each.value.id_token_validity
  refresh_token_validity = each.value.refresh_token_validity
}


resource "aws_cognito_identity_pool" "this" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }

  identity_pool_name               = "${var.common.project_code}-${var.common.environment}-${each.value.name}"
  allow_unauthenticated_identities = each.value.allow_unauthenticated_identities == "TRUE" ? true : false

  dynamic "cognito_identity_providers" {
    for_each = each.value.cognito_identity_providers_list
    content {
      client_id               = aws_cognito_user_pool_client.this["${cognito_identity_providers.value.user_pool_name}.${cognito_identity_providers.value.client_name}"].id
      provider_name           = "cognito-idp.${var.common.aws_region}.amazonaws.com/${aws_cognito_user_pool.this[cognito_identity_providers.value.user_pool_name].id}"
      server_side_token_check = cognito_identity_providers.value.server_side_token_check == "TRUE" ? true : false
    }
  }

  # supported_login_providers = {
  #   "graph.facebook.com"  = "7346241598935552"
  #   "accounts.google.com" = "123456789012.apps.googleusercontent.com"
  # }

  # saml_provider_arns           = [aws_iam_saml_provider.default.arn]
  # openid_connect_provider_arns = ["arn:aws:iam::123456789012:oidc-provider/id.example.com"]

  tags = var.common.default_tags
}

resource "aws_cognito_user_pool_domain" "this" {
  for_each      = { for key, value in var.cognito_user_pool_list : value.name => value }
  domain       = "${each.value.domain_name}-${var.common.environment}"
  user_pool_id = aws_cognito_user_pool.this[each.value.name].id
}

resource "aws_iam_role" "authenticated_role" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-authenticated-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "cognito-identity.amazonaws.com:aud" = aws_cognito_identity_pool.this[each.value.name].id
          },
          "ForAnyValue:StringLike" = {
            "cognito-identity.amazonaws.com:amr" = "authenticated"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "authenticated_policy" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  name = "${var.common.project_code}-${var.common.environment}-${each.value.name}-authenticated-policy"
  role = aws_iam_role.authenticated_role[each.value.name].name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "mobileanalytics:PutEvents",
          "cognito-sync:*",
          "cognito-identity:*",
        ],
        Resource = "*",
      },
      {
        Effect   = "Allow",
        Action   = "s3:*",
        Resource = "*",
      },
    ]
  })
}

resource "aws_cognito_identity_pool_roles_attachment" "admin_identity_pool_role_mapping" {
  for_each = { for key, value in var.cognito_identity_pool_list: value.name => value }
  identity_pool_id = aws_cognito_identity_pool.this[each.value.name].id
  roles = {
    authenticated = aws_iam_role.authenticated_role[each.value.name].arn
  }
}

output "cognito_user_pool_arns" {
  value = { for key, value in var.cognito_user_pool_list : value.name => aws_cognito_user_pool.this[value.name].arn }
}
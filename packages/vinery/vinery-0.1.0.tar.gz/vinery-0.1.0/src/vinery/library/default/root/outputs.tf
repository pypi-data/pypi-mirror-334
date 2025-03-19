/*locals {
  output_resources = { for env, resource in var.environments :
    env => {
      resource_group_name     = azurerm_resource_group.env[env].name
      resource_group_location = azurerm_resource_group.env[env].location

      subnet_id = azurerm_subnet.env_default[env].id

      adf_id = azurerm_data_factory.env[env].id
      adls_service_endpoints = {
        for k_adls, v_adls in local.map_of_storage_accounts : k_adls => (
          v_adls.create_new ?
          azurerm_storage_account.env_name[k_adls].primary_blob_endpoint :
          v_adls.blob_service_endpoint
        )
        if v_adls.environment == env
      }
      akv_id  = azurerm_key_vault.env[env].id
      dbw_id  = azurerm_databricks_workspace.env[env].id
      dbw_url = azurerm_databricks_workspace.env[env].workspace_url
    }
  }
}

output "resources" {
  value = local.output_resources
}
*/

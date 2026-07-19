import json

# Simulate a Keycloak Realm's Identity Provider configuration.
# In a real Keycloak setup, this data would be fetched via the Admin REST API.
# Each IdP has a name, type, and a simulated 'config_status' indicating its operational state.
# 'misconfigured' simulates a "failed login option" as described in the article.
realm_config = {
    "realm_name": "my-app-realm",
    "identity_providers": [
        {
            "alias": "google",
            "display_name": "Google Login",
            "provider_id": "google",
            "enabled": True,
            "config_status": "ok" # This simulates a healthy IdP
        },
        {
            "alias": "github",
            "display_name": "GitHub Login",
            "provider_id": "github",
            "enabled": True,
            "config_status": "misconfigured" # This simulates a "failed login option"
        },
        {
            "alias": "ldap",
            "display_name": "Corporate LDAP",
            "provider_id": "ldap",
            "enabled": True,
            "config_status": "ok"
        },
        {
            "alias": "facebook",
            "display_name": "Facebook Login",
            "provider_id": "facebook",
            "enabled": False, # Already disabled
            "config_status": "ok"
        },
        {
            "alias": "saml-external",
            "display_name": "External SAML IdP",
            "provider_id": "saml",
            "enabled": True,
            "config_status": "misconfigured" # Another "failed login option"
        }
    ]
}

def get_identity_providers(config):
    """Retrieves the list of identity providers from the simulated realm config."""
    return config["identity_providers"]

def identify_failed_login_options(idps):
    """
    Identifies identity providers that are enabled but misconfigured.
    This simulates detecting "failed login options" as per the article's context.
    """
    failed_options = []
    print("\n--- Identifying Failed Login Options ---")
    for idp in idps:
        if idp["enabled"] and idp["config_status"] == "misconfigured":
            print(f"  [!] Detected: '{idp['display_name']}' ({idp['alias']}) is enabled but misconfigured.")
            failed_options.append(idp)
        elif idp["enabled"]:
            print(f"  [OK] '{idp['display_name']}' ({idp['alias']}) is enabled and healthy.")
        else:
            print(f"  [INFO] '{idp['display_name']}' ({idp['alias']}) is disabled.")
    return failed_options

def disable_failed_login_option(idp_alias, config):
    """
    Simulates disabling a specific identity provider to fix a failed option.
    This is the core "fix" action demonstrated, preventing users from selecting it.
    In a real Keycloak setup, this would be an API call to update the IdP's 'enabled' status.
    """
    print(f"\n--- Attempting to fix '{idp_alias}' ---")
    for idp in config["identity_providers"]:
        if idp["alias"] == idp_alias:
            if idp["enabled"] and idp["config_status"] == "misconfigured":
                idp["enabled"] = False # The actual fix: disable the problematic IdP
                print(f"  [SUCCESS] '{idp['display_name']}' ({idp_alias}) has been disabled.")
                idp["config_status"] = "fixed-by-disabling" # Update status for clarity
                return True
            elif not idp["enabled"]:
                print(f"  [INFO] '{idp['display_name']}' ({idp_alias}) is already disabled.")
                return False
            else:
                print(f"  [INFO] '{idp['display_name']}' ({idp_alias}) is not misconfigured or already fixed.")
                return False
    print(f"  [ERROR] Identity Provider '{idp_alias}' not found.")
    return False

def print_current_status(config):
    """Prints the current status of all identity providers."""
    print("\n--- Current Identity Provider Status ---")
    for idp in config["identity_providers"]:
        status_str = "Enabled" if idp["enabled"] else "Disabled"
        config_str = idp["config_status"]
        print(f"  - {idp['display_name']} ({idp['alias']}): {status_str}, Config: {config_str}")

if __name__ == "__main__":
    print("Simulating Keycloak Identity Provider Management")
    print("Initial Configuration:")
    print(json.dumps(realm_config, indent=2))

    # Step 1: Identify currently failed login options
    current_idps = get_identity_providers(realm_config)
    failed_options_to_fix = identify_failed_login_options(current_idps)

    # Step 2: Attempt to fix them by disabling
    if failed_options_to_fix:
        print("\n--- Applying Fixes ---")
        for failed_idp in failed_options_to_fix:
            disable_failed_login_option(failed_idp["alias"], realm_config)
    else:
        print("\nNo misconfigured enabled login options found to fix.")

    # Step 3: Verify the changes
    print("\n--- Verification After Fixes ---")
    print_current_status(realm_config)

    # Re-run identification to confirm they are no longer detected as "failed"
    print("\n--- Re-identifying Failed Login Options (after fixes) ---")
    identify_failed_login_options(get_identity_providers(realm_config))

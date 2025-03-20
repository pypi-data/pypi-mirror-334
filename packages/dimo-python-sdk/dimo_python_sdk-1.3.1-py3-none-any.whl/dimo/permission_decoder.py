class PermissionDecoder:
    @staticmethod
    def decode_permission_bits(permission_hex: str) -> list:
        clean_hex = permission_hex.lower().replace("0x", "")
        permission_bits = int(clean_hex, 16)

        granted_permissions = []

        for i in range(128):
            bit_pair = (permission_bits >> i * 2) & 0b11
            if bit_pair == 0b11:
                granted_permissions.append(i)
        return granted_permissions

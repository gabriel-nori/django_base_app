PUBLIC_NAMESPACE = "public"
PRIVATE_NAMESPACE = "private"


def is_public_route(request) -> bool:
    """True when the resolved URL lives under the api/public/ namespace."""
    match = getattr(request, "resolver_match", None)
    return bool(match and PUBLIC_NAMESPACE in match.namespaces)

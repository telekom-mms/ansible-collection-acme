from ansible.errors import AnsibleError


def find_challenges(challenge_response: dict, challenge_type: str, expected_domains: list) -> dict:
    """
    1. check if all the expected domains are present in the challenge response
    2. construct and return the following dictionary out of the API response
       challenge_data and authorizations fields
       {'<domain>': {[http-01/dns-01]: 'resource': <http path/dns record'> resource_value': <token>}}
    """
    challenges = build_challenges(challenge_response, challenge_type, expected_domains)
    domains_in_response = find_domains_in_response(challenge_response, challenge_type)
    errors = []

    if domains_in_response == set(expected_domains):
        return challenges
    else:
        expected_not_found = set(expected_domains).difference(domains_in_response)
        if expected_not_found:
            errors.append(f"Expected {challenge_type} challenges for the following domains not found: "
                          f"{','.join(expected_not_found)}")

        unexpected_from_api = domains_in_response.difference(set(expected_domains))
        if unexpected_from_api:
            errors.append(f"The API responded with {challenge_type} challenges for the following domains "
                          f"we did not expect: {','.join(unexpected_from_api)}")
    if errors:
        raise AnsibleError(" // ".join(errors))

    return dict()


def find_domains_in_response(challenge_response: dict, challenge_type: str) -> set:
    """
    find the domains in the response for which the API responded with a challenge of the specified challenge_type
    """
    domains = set()
    for domain, domain_data in challenge_response['challenge_data'].items():
        if challenge_type in domain_data:
            domains.add(domain)

    for domain, domain_data in challenge_response['authorizations'].items():
        for challenge in domain_data['challenges']:
            if challenge['type'] == challenge_type:
                domains.add(domain)

    return domains


def build_challenges(challenge_response: dict, challenge_type: str, expected_domains: list) -> dict:
    """
    try to extract the challenge for all expected_domains from the challenge_data field (first)0
    and then from the authorization field, if not found
    """
    if challenge_type not in ['http-01', 'dns-01']:
        raise AssertionError(f"Unknown challenge_type ({challenge_type})")

    extracted_challenges = {}
    for domain in expected_domains:
        extracted_challenges[domain] = {}
        if domain in challenge_response['challenge_data']:
            extracted_challenges[domain] = extract_challenge_from_challenge_data(domain, challenge_response,
                                                                                 challenge_type)
        elif domain in challenge_response['authorizations']:
            extracted_challenges[domain] = extract_challenge_from_authorizations_data(domain, challenge_response,
                                                                                      challenge_type)

    return extracted_challenges


def extract_challenge_from_challenge_data(domain, challenge_response: dict, challenge_type: str) -> dict:
    """
    return the challenge data fields (record, resource, resource_value) out of the challenge_data field for domain
    """
    if challenge_type not in challenge_response['challenge_data'][domain]:
        raise AssertionError(f"challenge_type '{challenge_type}' not in 'challenge_data'")

    return {challenge_type: challenge_response['challenge_data'][domain][challenge_type]}


def extract_challenge_from_authorizations_data(domain, challenge_response: dict, challenge_type: str) -> dict:
    """
    return the challenge data fields from the authorizations field - note that the format is different from challange_data:
    the authorizations field specifies the challenges with their type in a list instead of a dict
    """
    if 'challenges' not in challenge_response['authorizations'][domain]:
        raise AssertionError(f"'challenges' missing in 'authorizations' field of domain '{domain}'")

    for challenge in challenge_response['authorizations'][domain]['challenges']:
        if challenge['type'] == challenge_type:
            if challenge_type == 'dns-01':
                return {challenge_type: build_data_from_authorizations_dns01(challenge['token'], domain)}
            elif challenge_type == 'http-01':
                return {challenge_type: build_data_from_authorizations_http01(challenge['token'], domain)}

    raise AssertionError(f"challenge_type '{challenge_type}' not in 'authorizations'")


def build_data_from_authorizations_dns01(token: str, domain: str) -> dict:
    """
    build the fields that one would expect out of challenge_data for data coming out of authorizations (for DNS-01)
    """
    return {
        "record": f"_acme-challenge.{domain}",
        "resource": "_acme-challenge",
        "resource_value": token
    }


def build_data_from_authorizations_http01(token: str, domain: str) -> dict:
    """
    build the fields that one would expect out of challange_data for data coming out of authorizations (for HTTP-01)
    """
    return {
        "resource": f".well-known/acme-challenge/{token}",
        "resource_value": token
    }


class FilterModule(object):
    """ utility filters for operating on dictionary """
    @staticmethod
    def filters():
        return {
            'find_challenges': find_challenges
        }

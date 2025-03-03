from ansible.errors import AnsibleError


def find_challenges(challenge_response: dict, challenge_type: str, expected_domains: list,
                    challenge_data_type: str = 'default') -> dict:
    challenges = build_challenges(challenge_response, challenge_type, challenge_data_type)

    if set(challenges.keys()) == set(expected_domains):
        return challenges
    else:
        errors = []
        expected_not_found = set(expected_domains).difference(set(challenges.keys()))
        if expected_not_found:
            errors.append(f"Expected {challenge_type} challenges for the following domains not found: "
                          f"{','.join(expected_not_found)}")

        unexpected_from_api = set(challenges.keys()).difference(set(expected_domains))
        if unexpected_from_api:
            errors.append(f"The API responded with {challenge_type} challenges for the following domains "
                          f"we did not expect: {','.join(unexpected_from_api)}")

        if errors:
            raise AnsibleError(" // ".join(errors))


def build_challenges(challenge_response: dict, challenge_type: str, challenge_data_type: str = 'default') -> dict:
    if challenge_type not in ['http-01', 'dns-01']:
        raise AssertionError(f"Unknown challenge_type ({challenge_type})")

    if challenge_data_type == 'default':
        if 'challenge_data' not in challenge_response:
            raise AssertionError("'challenge_data' field not in response.")

        return extract_challenges_from_challenge_data(challenge_response, challenge_type)

    elif challenge_data_type == 'with_authorizations':
        if 'challenge_data' not in challenge_response:
            raise AssertionError("'challenge_data' missing in API response")
        if 'authorizations' not in challenge_response:
            raise AssertionError("'authorizations' missing in API response")

        if len(challenge_response['challenge_data']) > 0:
            return extract_challenges_from_challenge_data(challenge_response, challenge_type)
        else:
            return extract_challenges_from_authorizations_data(challenge_response, challenge_type)
    else:
        raise AnsibleError(f"invalid challenge_data_type {challenge_data_type}")


def extract_challenges_from_challenge_data(challenge_response: dict, challenge_type: str) -> dict:
    re = {}
    for domain, domain_data in challenge_response['challenge_data'].items():
        if challenge_type not in domain_data:
            raise AssertionError(f"challenge_type '{challenge_type}' not in 'challenge_data'")

        re[domain] = {}
        re[domain][challenge_type] = domain_data[challenge_type]

    return re


def extract_challenges_from_authorizations_data(challenge_response: dict, challenge_type: str):
    re = {}
    for domain, domain_data in challenge_response['authorizations'].items():
        if 'challenges' not in challenge_response['authorizations'][domain]:
            raise AssertionError(f"'challenges' missing for '{domain}' in API response")

        for challenge in challenge_response['authorizations'][domain]['challenges']:
            if challenge['type'] == challenge_type:
                re[domain] = {}
                if challenge_type == 'dns-01':
                    re[domain][challenge_type] = build_data_from_authorizations_dns01(challenge['token'], domain)
                elif challenge_type == 'http-01':
                    re[domain][challenge_type] = build_data_from_authorizations_http01(challenge['token'], domain)
    return re


def build_data_from_authorizations_dns01(token: str, domain: str) -> dict:
    return {
        "record": f"_acme-challenge.{domain}",
        "resource": "_acme-challenge",
        "resource_value": token
    }


def build_data_from_authorizations_http01(token: str, domain: str) -> dict:
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

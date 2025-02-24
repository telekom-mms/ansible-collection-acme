from ansible.errors import AnsibleError


def find_challenges(challenge_response: dict, challenge_type: str, expected_domains: list,
                    challenge_data_type: str = 'default') -> dict:
    challenges = build_challenges(challenge_response, challenge_type, challenge_data_type)

    if set(challenges.keys()) == set(expected_domains):
        return challenges
    else:
        expected_not_found = set(expected_domains).difference(set(challenges.keys()))
        unexpected_from_api = set(challenges.keys()).difference(set(expected_domains))
        raise AnsibleError(f"Unexpected challenges found: "
                           f"(expected_not_found={expected_not_found} // unexpected_from_api={unexpected_from_api})")


def build_challenges(challenge_response: dict, challenge_type: str, challenge_data_type: str = 'default') -> dict:
    assert challenge_type in ['http-01', 'dns-01'], f"Unknown challenge_type ({challenge_type})"

    if challenge_data_type == 'default':
        assert 'challenge_data' in challenge_response
        return extract_challenges_from_challenge_data(challenge_response, challenge_type)

    elif challenge_data_type == 'telesec':
        assert 'challenge_data' in challenge_response, "'challenge_data' missing in API response"
        assert 'authorizations' in challenge_response, "'authorizations' missing in API response"
        if len(challenge_response['challenge_data']) > 0:
            return extract_challenges_from_challenge_data(challenge_response, challenge_type)
        else:
            return extract_challenges_from_authorizations_data(challenge_response, challenge_type)
    else:
        raise AnsibleError(f"invalid challenge_data_type {challenge_data_type}")


def extract_challenges_from_challenge_data(challenge_response: dict, challenge_type: str) -> dict:
    re = {}
    for domain, domain_data in challenge_response['challenge_data'].items():
        assert challenge_type in domain_data
        re[domain] = {}
        re[domain][challenge_type] = domain_data[challenge_type]

    return re


def extract_challenges_from_authorizations_data(challenge_response: dict, challenge_type: str):
    re = {}
    for domain, domain_data in challenge_response['authorizations'].items():
        assert 'challenges' in challenge_response['authorizations'][domain], f"'challenges' missing for '{domain}'"

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

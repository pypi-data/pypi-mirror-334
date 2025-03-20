"""Gitlab API utilities"""

import requests

DEFAULT_TIMEOUT_SECONDS = 30

class GitlabApiClient:
    """Gitlab API client"""
    def __init__(self, gitlab_url, access_token):
        self.gitlab_url = gitlab_url.strip('/')
        self.access_token = access_token


    def get_subgroup_ids(self, group_id):
        """Get the subgroups of the given group_id."""
        response = requests.get(
            f'{self.gitlab_url}/api/v4/groups/{group_id}/subgroups',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        assert response.status_code == 200, response.text

        return [group['id'] for group in response.json()]


    def get_project_ids(self, group_id):
        """Get the projects of the given group_id."""
        response = requests.get(
            f'{self.gitlab_url}/api/v4/groups/{group_id}/projects', 
            headers={
                'Authorization': f'Bearer {self.access_token}'
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        assert response.status_code == 200, response.text

        return [project['id'] for project in response.json()]


    def get_merge_request_urls_by_project_id(self, project_id, state=None):
        """Get the merge request urls of the given project_id."""
        return self.get_merge_request_fields_by_project_id(project_id, state=state, fields=["web_url"])


    def get_merge_request_fields_by_project_id(self, project_id, state=None, fields=[]):
        """Get specific fields from merge requests of the given project_id."""
        merge_requests = self.get_merge_requests_by_project_id(project_id, state=state)

        if not fields:
            return merge_requests

        return [{field: merge_request[field] for field in fields if field in merge_request}
                for merge_request in merge_requests]


    def get_merge_requests_by_project_id(self, project_id, state=None):
        """Get the merge requests of the given project_id."""

        params = {}
        if state:
            params['state'] = state

        response = requests.get(
            f'{self.gitlab_url}/api/v4/projects/{project_id}/merge_requests', 
            headers={
                'Authorization': f'Bearer {self.access_token}'
            },
            params=params,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error fetching merge requests: {response.status_code} - {response.text}')
            return []


    def get_merge_request_urls_by_group_id(self, group_id, state=None):
        """Get all merge requests in the subgroups of the given parent_group_id."""
        merge_requests = []

        subgroup_ids = self.get_subgroup_ids(group_id)
        subgroup_ids.append(group_id)
        for subgroup_id in subgroup_ids:
            # 2. 하위 그룹의 프로젝트 목록 가져오기
            project_ids = self.get_project_ids(subgroup_id)

            for project_id in project_ids:
                # 3. 각 프로젝트의 Merge Requests 가져오기
                merge_requests.extend(self.get_merge_request_urls_by_project_id(project_id, state=state))

        return merge_requests

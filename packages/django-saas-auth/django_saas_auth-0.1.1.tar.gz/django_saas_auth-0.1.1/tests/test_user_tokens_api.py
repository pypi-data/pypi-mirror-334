from saas_base.test import SaasTestCase
from saas_auth.models import UserToken


class TestUserTokensAPI(SaasTestCase):
    user_id = SaasTestCase.OWNER_USER_ID

    def create_user_tokens(self, count=4):
        items = []
        for i in range(count):
            token = UserToken.objects.create(
                name=f'Foo {i}',
                scope='__all__',
                user_id=self.user_id,
            )
            items.append(token)
        return items

    def test_create_user_token_with_scope(self):
        self.force_login()
        data = {'name': 'foo', 'scope': '__all__'}
        resp = self.client.post('/api/user/tokens/', data=data, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_create_user_token_without_scope(self):
        self.force_login()
        data = {'name': 'foo'}
        resp = self.client.post('/api/user/tokens/', data=data, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_create_user_token_with_key(self):
        self.force_login()
        data = {'name': 'foo', 'scope': '__all__', 'key': 'bar'}
        resp = self.client.post('/api/user/tokens/', data=data, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertNotEqual(data['key'], 'bar')

    def test_list_user_tokens(self):
        self.force_login()
        self.create_user_tokens()
        resp = self.client.get('/api/user/tokens/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 4)

    def test_delete_user_token(self):
        self.force_login()
        items = self.create_user_tokens()
        token_id = items[0].id
        resp = self.client.delete(f'/api/user/tokens/{token_id}/')
        self.assertEqual(resp.status_code, 204)
        count = UserToken.objects.filter(user_id=self.user_id).count()
        self.assertEqual(count, 3)

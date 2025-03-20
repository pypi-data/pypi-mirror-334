from typing import Literal, assert_type
import json

from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from thelabtyping.api.requests import (
    AuthdEmptyTypedRequest,
    AuthdTypedRequest,
    AuthdTypedRequestBody,
    AuthdTypedRequestQuery,
    EmptyTypedRequest,
    TypedRequest,
    TypedRequestBody,
)
from thelabtyping.api.responses import APIResponse
from thelabtyping.api.serializers import Empty
from thelabtyping.api.status import Status
from thelabtyping.api.views import validate

from ..sampleapp.serializers import APIUser, UserSearchQuery


class APIViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="joe", password="password")
        self.client = Client()

    def test_list_users(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list"))
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            [
                {
                    "username": "joe",
                    "first_name": "",
                    "last_name": "",
                }
            ],
        )

    def test_list_users_with_filter(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list") + "?first_name=Jim")
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, [])

    def test_list_users_with_invalid_filter(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list") + "?id=FOO")
        self.assertEqual(resp.status_code, Status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            resp.content,
            {
                "errors": {
                    "id": {
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "type": "int_parsing",
                    }
                }
            },
        )

    def test_create_user(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            {
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )

    def test_create_user_urlencoded(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            {
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )

    def test_create_user_invalid_body(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data={
                "username": "jack",
                "first_name": "Jack",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            resp.content,
            {
                "errors": {
                    "last_name": {
                        "msg": "Field required",
                        "type": "missing",
                    },
                },
            },
        )

    def test_create_user_without_login(self) -> None:
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data=json.dumps(
                {
                    "username": "jack",
                    "first_name": "Jack",
                    "last_name": "Jackson",
                }
            ),
        )
        self.assertEqual(resp.status_code, Status.HTTP_403_FORBIDDEN)

    def test_typed_request(self) -> None:
        @validate()
        def view(
            request: TypedRequest[UserSearchQuery, APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, APIUser])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_typed_request_body(self) -> None:
        @validate()
        def view(
            request: TypedRequestBody[APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, APIUser])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_empty_request(self) -> None:
        @validate()
        def view(
            request: EmptyTypedRequest,
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, Empty])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequest[UserSearchQuery, APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, APIUser, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_query(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequestQuery[UserSearchQuery],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, Empty, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_body(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequestBody[APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, APIUser, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_empty(self) -> None:
        @validate()
        def view(
            request: AuthdEmptyTypedRequest,
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, Empty, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_invalid_request_type(self) -> None:
        with self.assertRaises(TypeError):

            @validate()
            def view(
                request: HttpRequest,
            ) -> APIResponse[Empty]:
                # Some assertions to prove the `validate` decorator is doing what it's
                # supposed to
                assert_type(request, HttpRequest)
                assert_type(request.user, User | AnonymousUser)
                return APIResponse(Empty())

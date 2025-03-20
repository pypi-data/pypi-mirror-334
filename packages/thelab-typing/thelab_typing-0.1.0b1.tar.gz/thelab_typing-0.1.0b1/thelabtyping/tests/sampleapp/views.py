from typing import Literal, assert_type

from django.contrib.auth.models import AnonymousUser, User
from django.utils.decorators import method_decorator
from django.views.generic import View

from thelabtyping.abc import ListOf
from thelabtyping.api.requests import (
    AuthdEmptyTypedRequest,
    AuthdTypedRequest,
    AuthdTypedRequestBody,
    AuthdTypedRequestQuery,
    EmptyTypedRequest,
    TypedRequest,
    TypedRequestBody,
    TypedRequestQuery,
)
from thelabtyping.api.responses import APIResponse
from thelabtyping.api.serializers import Empty
from thelabtyping.api.views import validate

from .serializers import APIUser, UserSearchQuery


class UserView(View):
    @method_decorator(validate())
    def get(
        self, request: TypedRequestQuery[UserSearchQuery]
    ) -> APIResponse[ListOf[APIUser]]:
        # Some assertions to prove the `validate` decorator is doing what it's
        # supposed to
        assert_type(request, TypedRequest[UserSearchQuery, Empty])
        assert_type(request.user, User | AnonymousUser)
        assert_type(request.validated_querystring, UserSearchQuery)
        assert_type(request.validated_body, Empty)
        # Do the same checks at runtime
        assert isinstance(request, TypedRequest)
        assert isinstance(request.user, (User | AnonymousUser))
        assert isinstance(request.validated_querystring, UserSearchQuery)
        assert isinstance(request.validated_body, Empty)
        # Use the UserSearchQuery model to get he queryset of users to return
        users, errs = APIUser.list_from_django(
            request,
            request.validated_querystring.get_queryset(),
        )
        return APIResponse(users)

    @method_decorator(validate())
    def post(self, request: AuthdTypedRequestBody[APIUser]) -> APIResponse[APIUser]:
        # Some assertions to prove the `validate` decorator is doing what it's
        # supposed to
        assert_type(request, TypedRequest[Empty, APIUser, User])
        assert_type(request.user, User)
        assert_type(request.validated_querystring, Empty)
        assert_type(request.validated_body, APIUser)
        # Do the same checks at runtime
        assert isinstance(request, TypedRequest)
        assert isinstance(request.user, User)
        assert isinstance(request.validated_querystring, Empty)
        assert isinstance(request.validated_body, APIUser)
        # Save the user model and return it
        result = (
            # Take the input data
            request.validated_body
            # Create the Django user
            .create(request)
            # Then serialize it back into an APIUser
            .and_then(lambda djuser: APIUser.from_django(request, djuser))
        )
        return APIResponse(result)


@validate()
def get_test_typed_request_body(
    request: TypedRequestBody[APIUser],
) -> APIResponse[Empty]:
    # Some assertions to prove the `validate` decorator is doing what it's
    # supposed to
    assert_type(request, TypedRequest[Empty, APIUser])
    assert_type(request.user, User | AnonymousUser)
    assert_type(request.validated_querystring, Empty)
    assert_type(request.validated_body, APIUser)
    return APIResponse(Empty())


@validate()
def get_test_empty_request(request: EmptyTypedRequest) -> APIResponse[Empty]:
    # Some assertions to prove the `validate` decorator is doing what it's
    # supposed to
    assert_type(request, TypedRequest[Empty, Empty])
    assert_type(request.user, User | AnonymousUser)
    assert_type(request.validated_querystring, Empty)
    assert_type(request.validated_body, Empty)
    return APIResponse(Empty())


@validate()
def get_test_authd_typed_request(
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


@validate()
def get_test_authd_typed_request_query(
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


@validate()
def get_test_authd_typed_request_body(
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


@validate()
def get_test_authd_typed_request_empty(
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

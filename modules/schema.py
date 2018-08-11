#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import graphene
from graphene import ObjectType, Schema

class Query(ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f'Hello {name}'

class QueryRoot(ObjectType):

    thrower = graphene.String(required=True)
    request = graphene.String(required=True)
    test = graphene.String(who=graphene.String())

    def resolve_thrower(self, info):
        raise Exception("Throws!")

    def resolve_request(self, info):
        return info.context.arguments['q'][0]

    def resolve_test(self, info, who=None):
        return 'Hello %s' % (who or 'World')


class MutationRoot(ObjectType):
    write_test = graphene.Field(QueryRoot)

    def resolve_write_test(self, info):
        return QueryRoot()


# schema = Schema(query=QueryRoot, mutation=MutationRoot)
schema = Schema(query=Query)
# result = schema.execute('{ hello }')

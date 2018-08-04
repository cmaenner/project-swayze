import graphene

class Query(graphene.ObjectType):
    schema = None
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        self.set_header('Content-Type', 'application/json')
        self.write(f'Hello {name}')
        self.finish()

schema = graphene.Schema(query=Query)
schema.execute('{ hello }')

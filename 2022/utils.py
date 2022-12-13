def log(f):
    def call(*inputs):
        output = f(*inputs)

        print(f'{inputs}: {output}')

        return output

    return call

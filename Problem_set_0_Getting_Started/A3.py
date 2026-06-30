class ConsumerClass:
    """A consumer with Cobb-Douglas demand."""

    def __init__(self,I=10.0,p1=1.0,p2=2.0):
        """Store income and prices as attributes (with defaults)."""

        self.I = I
        self.p1 = p1
        self.p2 = p2

    def demand(self,alpha):
        """Return the Cobb-Douglas demands (x1,x2) for a given alpha."""

        x1 = alpha*self.I/self.p1
        x2 = (1-alpha)*self.I/self.p2
        return x1,x2

    def __str__(self):
        """Return a readable summary of the consumer."""

        return f'ConsumerClass(I={self.I}, p1={self.p1}, p2={self.p2})'


def solve():
    """Create two consumers with different incomes and print their demands for alpha=0.5."""

    consumers = [ConsumerClass(I=10.0),ConsumerClass(I=20.0)]
    for consumer in consumers:
        x1,x2 = consumer.demand(0.5)
        print(f'{consumer} -> demand(0.5) = ({x1:.2f}, {x2:.2f})')

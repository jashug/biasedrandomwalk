from fractions import Fraction
import numbers, operator

# Most of our work is done in the field Q[phi]

class PhiNum(numbers.Real):
    """Represents numbers in the form a + b phi"""
    # We typically assume a and b are either int or Fraction
    # Implementation modelled on stdlib fractions.Fraction

    __slots__ = ('rat', 'alg')

    def __init__(self, rat, alg=0):
        """Constructs a PhiNum equal to rat + alg * phi"""
        # Could return rat from __new__ when alg is 0, cool but no point
        if isinstance(rat, PhiNum) or isinstance(alg, PhiNum):
            raise TypeError("The constructor does not accept PhiNum")
        self.rat = rat
        self.alg = alg

    def __repr__(self):
        return "{!r} + {!r} * phi".format(self.rat, self.alg)

    def __str__(self):
        if self.alg:
            return "{} + {} * phi".format(self.rat, self.alg)
        else:
            return str(self.rat)

    def __float__(self):
        return float(self.rat) + float(self.alg) * (1 + 5**.5)/2

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        """Generates forward and reverse operators given a purely-phinum
        operator and a function from the operator module.

        Use this like:
        __op__,__rop__ = _operator_fallbacks(just_rational_op, operator.op)

        We coerce int, Fraction to PhiNum, and do not coerce PhiNum to anything.
        When used with ints or fractions of ints, these coercions are non-lossy.

        The fallback operator is not actually used except for its name,
        since we do not currently coerce PhiNum to anything.
        """

        def forward(a, b):
            if isinstance(b, PhiNum):
                return monomorphic_operator(a, b)
            elif isinstance(b, (int, Fraction)):
                return monomorphic_operator(a, PhiNum(b))
            else:
                return NotImplemented
        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, PhiNum):
                return monomorphic_operator(a, b)
            elif isinstance(a, (int, Fraction)):
                return monomorphic_operator(PhiNum(a), b)
            else:
                return NotImplemented
        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(a, b):
        """a + b"""
        return PhiNum(a.rat + b.rat, a.alg + b.alg)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(a, b):
        """a - b"""
        return PhiNum(a.rat - b.rat, a.alg - b.alg)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(a, b):
        """a * b"""
        phi2 = a.alg * b.alg
        return PhiNum(a.rat * b.rat + phi2, a.rat * b.alg + a.alg * b.rat + phi2)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def inv(a):
        denom = a.rat**2 + a.rat * a.alg - a.alg ** 2
        return PhiNum(Fraction(a.rat + a.alg, denom), Fraction(- a.alg, denom))

    def _div(a, b):
        """a / b"""
        return a * b.inv()

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def __floordiv__(a, b):
        return NotImplemented

    def __rfloordiv__(b, a):
        return NotImplemented

    def __mod__(a, b):
        return NotImplemented

    def __rmod__(b, a):
        return NotImplemented

    def __pow__(a, b):
        """a ** b"""
        if isinstance(b, numbers.Integral):
            if b < 0:
                b = - b
                a = a.inv()
            res = PhiNum(1, 0)
            while b >= 1:
                if b % 2 == 0:
                    a = a * a
                    b = b // 2
                else:
                    res = a * res
                    a = a * a
                    b = (b - 1) // 2
            return res
        else:
            return NotImplemented

    def __rpow__(b, a):
        return NotImplemented

    def __pos__(a):
        """+a: Coerces a subclass instance to PhiNum"""
        return PhiNum(a.rat, a.alg)

    def __neg__(a):
        """-a"""
        return PhiNum(-a.rat, -a.alg)

    def __abs__(a):
        raise NotImplementedError

    def __trunc__(a):
        raise NotImplementedError

    def __floor__(a):
        raise NotImplementedError

    def __ceil__(a):
        raise NotImplementedError

    def __round__(a):
        raise NotImplementedError

    def __le__(a, b):
        raise NotImplementedError

    def __lt__(a, b):
        raise NotImplementedError

    def __eq__(a, b):
        """a == b

        We only know how to compare to int, Fraction, PhiNum
        """
        if isinstance(b, PhiNum):
            return a.rat == b.rat and a.alg == b.alg
        elif isinstance(b, (int, Fraction)):
            return a.rat == b and a.alg == 0
        else:
            return NotImplemented

    # No order comparisons

    def __bool__(a):
        """a != 0"""
        return a.rat != 0 or a.alg != 0

    def exact_rat(a):
        assert a.alg == 0
        return a.rat

    def exact_int(a):
        out = a.exact_rat()
        assert out.denominator == 1
        return out.numerator

phi = PhiNum(0, 1)
sqrt5 = 2 * phi - 1

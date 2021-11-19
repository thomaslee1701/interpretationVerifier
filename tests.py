from verify_interpretations import *

UD = (1, 2, 3)
interpretation = {
    'F':(1, 2),
    'G':([1, 2], [3, 1]),
    'H':(1, 2, 3),
    'A':([1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]),
    'B':([1, 2], [2, 1], [3, 1]),
    'C':([1,1], [3,2]),
    'E':()
}

"""
unittests for isin
"""

v = Verify(interpretation, UD)

assert(v.isin('F', 1))
assert(not v.isin('F', 3))
assert(v.isin('G', [1,2]))

"""
unittests for isSingleSet
"""
assert(v.isSingleSet('F{abc}'))
assert(v.isSingleSet('G{ab}'))
assert(v.isSingleSet('F{a}'))
assert(not v.isSingleSet('F{a}.G{b}'))
assert(not v.isSingleSet('F{a}.G{b}'))
assert(not v.isSingleSet('F{a}>G{b}'))
assert(not v.isSingleSet('F{a}.G{b}.H{c}'))

"""
unittests for verify for a single set
"""
v.values_dict['x'] = 1 # manually put the number 1 in as x
v.values_dict['y'] = 2
assert(v.verify('F{x}'))
assert(v.verify('G{xy}'))
v.values_dict['y'] = 3
assert(not v.verify('G{xy}'))
v.values_dict = {}

"""
unittests for ForAll and Exists
"""
assert(v.verify('ForAllx(H{x})'))
assert(not v.verify('ForAllx(F{x})'))
assert(v.verify('Existsx(H{x})'))
assert(v.verify('Existsx(F{x})'))
assert(v.verify('ForAllx(ForAlly(A{xy}))'))

"""
unittests for .
"""
assert(v.verify('Existsx((H{x}).(F{x}))'))
assert(not v.verify('Existsx((H{x}).(E{x}))'))
assert(v.verify('( ForAllx(H{x}) ).( Existsy(F{y}) )'))
assert(not v.verify('( ForAllx(H{x}) ).( ForAlly(F{y}) )'))
assert(v.verify('ForAllx(Existsy((B{xy}).(H{x})))'))

"""
unittests for v
"""
assert(v.verify('Existsx((H{x})v(E{x}))'))
assert(not v.verify('Existsx((E{x})v(E{x}))'))
assert(v.verify('( ForAllx(H{x}) )v( Existsy(E{y}) )'))
assert(v.verify('ForAllx(Existsy((B{xy})v(H{y})))'))

"""
unittests for >
"""
assert(v.verify('ForAll x ((F{x})>(H{x}))'))
assert(not v.verify('ForAllx((H{x})>(E{x}))'))
assert(v.verify('ForAll x ((E{x})>(H{x}))'))
assert(v.verify('ForAllx(ForAlly((C{xy})>(F{y})))'))
assert(not v.verify('ForAllx(ForAlly((C{xy})>(F{x})))'))

"""
unittests for -
"""
assert(not v.verify('-(ForAll x ((F{x})>(H{x})))'))
assert(v.verify('-(ForAllx((H{x})>(E{x})))'))
assert(not v.verify('-(ForAll x ((E{x})>(H{x})))'))
assert(not v.verify('-(ForAllx(ForAlly((C{xy})>(F{y}))))'))
assert(v.verify('-(ForAllx(ForAlly((C{xy})>(F{x}))))'))


"""
Tests from homework
"""
def homeworkTests1():
    UD = (1, 2, 3)
    interpretation = {
    'F':(1, 2),
    'G':(2, 3),
    }
    v = Verify(interpretation, UD)
    str1 = 'existsx((F{x})=(G{x}))'
    str2 = '-(forally( (F{y})>(G{y}) ))'
    str3  = '-(forallz((G{z})>(F{z})))'
    query = f'(({str1}).({str2})).({str3})'
    assert(v.verify(query)) # (∃x)(Fx≡Gx).-(∀x)(Fx⊃Gx).-(∀x)(Gx⊃Fx) 

def homeworkTests2():
    UD = (1, 2, 3)
    interpretation = {
    'F':(1, 2),
    'G':(2, 3),
    'H':(2)
    }
    v = Verify(interpretation, UD)
    str1 = 'forallx( ( (F{x}).(G{x}) )>(H{x})  )'
    str2 = '-(forally( (F{y}) > ((G{y}).(H{y})) ))'
    str3  = '-(forallz((G{z})>( (F{z}).(H{z}) )))'
    assert(v.verify(str1))
    assert(v.verify(str2))
    assert(v.verify(str3))
    query = f'(({str1}).({str2})).({str3})'
    assert(v.verify(query)) # (∀x)(Fx.Gx ⊃ Hx).-(∀x)(Fx ⊃ Gx.Hx).-(∀x)(Gx ⊃ Fx.Hx) 



print('All tests passed!')

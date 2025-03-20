***,{name}
memory,1600,M
orient
geomtyp=xyz
geometry={{
{natom}
{name}
{geom}
}}
{{uhf;wf,{nelectron},{symm},{spin},{charge}}}

basis=cc-pvdz-f12
rhf
CCSD(T)-F12

mydza = energy(1)
mydzb = energy(2)

basis=cc-pvtz-f12
rhf
CCSD(T)-F12

mytza = energy(1)
mytzb = energy(2)
---


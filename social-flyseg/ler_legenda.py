"""Uso: python3 legenda.py <pasta> "<cabeçalho>"  -> imprime a legenda exata da seção."""
import re,sys
d,h=sys.argv[1],sys.argv[2]
t=open(f"/home/claude/flycomp-midia/social-flyseg/{d}/legenda.md").read()
m=re.search(r"^"+re.escape(h)+r"\n\n(.*?)(?=\n#{2,3} |\Z)",t,re.S|re.M)
print(m.group(1).strip())

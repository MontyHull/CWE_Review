#!/bin/bash --norc

set -e
set -u

srcdir=$(dirname "$(readlink -f "$0")")

function usage {
  echo "Usage: $0 n f"
  echo "  n files named z3inXXXXX.txt will be saved to folder f."
  [[ $# -eq 1 ]] && exit $1
}

[[ $# -eq 2 ]] || usage 1

num=$1
outfold=$(readlink -f "$2")
mkdir -p "$outfold"

temp="temp33gen.txt"

cd "$srcdir"
i=0
while [[ $i -lt $num ]]; do
  outfile="$outfold/z3in$(printf '%05d' $i).txt"
  if [[ -s $outfile ]]; then
    echo -n "."
    i=$(( i + 1 ))
  elif sage det33.sage "$outfile" >&/dev/null; then
    echo >"$temp"
    z3 -T:30 "$outfile" >& "$temp" || true
    if [[ $(head -1l "$temp") = "timeout" ]]; then
      echo -n "+"
      i=$(( i + 1 ))
    elif [[ $(head -1l "$temp") = "unsat" ]]; then
      rm -f "$outfile"
      :
    else
      echo
      echo "SOMETHING HAPPENED with $i $outfile $temp"
      exit 2
    fi
  else
    rm -f "$outfile"
  fi
done

rm "$temp"

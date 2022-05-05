# Decaf Compiler

## Team
1. AmirHosein Rostami 96101635
2. Arvin Ghavidel 96110583

## How to install
1. install python3
2. install lark-parser (v0.12.0)
if you do have anaconda try this:
```
conda install -c conda-forge lark-parser
```
## How to run
1. in the current directory simply run:
```
./run.sh
```

## Project Structure
```
TODO
```

## Updates
1. Since Decaf's documentation changed a lot, we updated our code and since there 
wasn't any other updated test cases for phase1, we updated phase1's test cases in a following way:
   1. We still support #define macros in the way as it was before.
   2. __func__ & __line__ keywords are removed and since they are not valid IDs, any testcase which has these keywords, at the moment of tokenizing them, outputs UNDEFINED_TOKEN and stops.
   3. += -= *= /= operators are removed and whenever there were for example += in testcases, we treat them as + Token and = Token.
   4. Obviously they forgot to include "{" and "}" characters as punctuation chars so we keep them as the way it was in the previous doc.
   5. Obviously they also forgot "&&" operator, so we keep it too as the way it was in the previous doc.
2. Updated testcases are attached.
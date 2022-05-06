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
### Phase 1
In the root directory simply do:
```
cd phase1
./run.sh
```
### Phase 2
In the root directory simply do:
```
cd phase2
./run.sh
```

## Project Structure
```
TODO
```

## Updates
### Phase 1
1. Since Decaf's documentation changed a lot, we updated our code and since there 
wasn't any other updated test cases for phase1, we updated phase1's test cases in a following way:
   1. We still support #define macros in the way as it was before.
   2. __func__ & __line__ keywords are removed and since they are not valid IDs, any testcase which has these keywords, at the moment of tokenizing them, outputs UNDEFINED_TOKEN and stops.
   3. += -= *= /= operators are removed and whenever there were for example += in testcases, we treat them as + Token and = Token.
   4. Obviously they forgot to include "{" and "}" characters as punctuation chars so we keep them as the way it was in the previous doc.
   5. Obviously they also forgot "&&" operator, so we keep it too as the way it was in the previous doc.
2. Updated testcases are attached.
### Phase 2
1. There were 27 wrong testcases(according to latest version of the project documents)
   1. wrong testcases = 
```
   [1,4,6,10,67,84,153,154,183,
   184,187,195,205,208,214,215,216,217,
   219,220,222,226,227,228,229,230,231]
```
2. I editted these 27 wrong testcases's .out files in order to make them true :).
3. Since some good testcases went to syntax error according to stupid mismatches with the latest docs, I corrected them and added 27 **new** test cases in order to make sure parser works fine, newly added testcases are:
```
   ["t1","t4","t6","t10","t67","t84","t153","t154","t183",
   "t184","t187","t195","t205","t208","t214","t215","t216","t217",
   "t219","t220","t222","t226","t227","t228","t229","t230","t231"]
```




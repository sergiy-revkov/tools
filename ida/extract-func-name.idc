#include <idc.idc>


static extract_func_name(s) {
  auto b, e, f;
  f = "";
  b = strstr(s, "\"");
  e = strlen(s);
  if (b != -1) {
    s = substr(s, b+1, e);
    e = strstr(s, "\"");
    if (e != -1) {
      f = substr(s, 0, e);
    }
  }
  return f;
}

static main() {
  auto func_name, disas, target, xref, addr, end, args, locals, frame, firstArg, name, ret, count, inst;
  addr = 0;
  for (addr = NextFunction(addr); addr != BADADDR; addr = NextFunction(addr)) {
    name = Name(addr);
    end = GetFunctionAttr(addr, FUNCATTR_END);
    count = 0;
    inst = addr;
    while (inst < end) {
      count++;
      inst = FindCode(inst, SEARCH_DOWN | SEARCH_NEXT);
      if (inst != -1) {
        disas = GetDisasm(inst);
        if (strstr(disas, "lea     rdx") != -1) {
          func_name = form("0x%x: %s\n",inst, disas);
        }
        for (target = Rfirst(inst); target!=BADADDR; target = Rnext(inst, target)) {
          xref = XrefType();
          if ((xref == fl_CN || xref == fl_CF) && Name(target) == "print_error") {
            Message ("%s calls %s from 0x%x with %s\n", name, Name(target), inst, extract_func_name(func_name));
            MakeNameEx(addr, extract_func_name(func_name), SN_NOCHECK);
          }
        }
      }
      else {
        break;
      }
    }
  }

  Message("----FINISHED----\n");
}

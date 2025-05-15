import pandas


ultimate_columns = ["id", "heimild", "nafn_norm", "first_name", "middle_name", "patronym", "surname", "birthyear",
                    "sex", "status", "marriagestatus", "person", "partner", "father", "mother", "source_partner",
                    "source_father", "source_mother", "source_farm", "farm", "county", "parish", "district"]
ultimate_ban_list = ["id", "partner", "father", "mother", "source_partner", "source_father", "source_mother",
                     "source_farm"]


class Truth:

    def __init__(self, f, c):
        self.f = f
        self.c = max(min(c, 0.99), 0.01)

    @property
    def wp(self):
        return self.f * self.c / (1 - self.c)

    @property
    def wn(self):
        return (1 - self.f) * self.c / (1 - self.c)

    def revise(self, truth):  # not in-place
        wp = self.wp + truth.wp
        wn = self.wn + truth.wn
        f = wp / (wp + wn)
        c = (wp + wn) / (wp + wn + 1)
        return Truth(f, c)

    @property
    def e(self):
        return self.c * (self.f - 0.5) + 0.5


def preprocessing_ultimate(row_1, row_2):
    # turn two rows into a bunch of formal representations
    ret = set()
    label = -1
    isna_row_1 = pandas.isna(row_1)
    isna_row_2 = pandas.isna(row_2)
    for i in range(len(ultimate_columns)):
        if ultimate_columns[i] == "heimild":
            if not isna_row_1[i] and not isna_row_2[i]:
                dif = str(abs(float(row_1[i]) - float(row_2[i])))
                ret.add("heimild_differ_in_" + dif + "_years")
        elif ultimate_columns[i] == "nafn_norm":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_name")
                else:
                    ret.add("different_name")
        elif ultimate_columns[i] == "first_name":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_first_name")
                else:
                    ret.add("different_first_name")
        elif ultimate_columns[i] == "patronym":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_last_name")
                else:
                    ret.add("different_last_name")
        elif ultimate_columns[i] == "surname":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_surname")
                else:
                    ret.add("different_surname")
        elif ultimate_columns[i] == "birthyear":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_birth_year")
                else:
                    ret.add("different_birth_year")
        elif ultimate_columns[i] == "sex":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_gender")
                else:
                    ret.add("different_gender")
        elif ultimate_columns[i] == "status":
            if not pandas.isna(row_1[i]):
                ret.add("social_status_is_" + row_1[i])
            if not pandas.isna(row_2[i]):
                ret.add("social_status_is_" + row_2[i])
        elif ultimate_columns[i] == "marriagestatus":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_marriage_status")
                else:
                    ret.add("different_marriage_status")
        elif ultimate_columns[i] == "farm":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_farm")
                else:
                    ret.add("different_farm")
        elif ultimate_columns[i] == "county":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_county")
                else:
                    ret.add("different_county")
        elif ultimate_columns[i] == "parish":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_parish")
                else:
                    ret.add("different_parish")
        elif ultimate_columns[i] == "district":
            if not isna_row_1[i] and not isna_row_2[i]:
                if row_1[i] == row_2[i]:
                    ret.add("same_district")
                else:
                    ret.add("different_district")
        elif ultimate_columns[i] == "person":
            if not isna_row_1[i] and not isna_row_2[i]:
                label = 1 if row_1[i] == row_2[i] else 0
            else:
                return None

    return Pattern(ret, Truth(label, 0.9))


class Pattern:

    def __init__(self, statements, truth):
        self.statements = frozenset(statements)
        self._hash = hash(self.statements)
        self.truth = truth

    def __len__(self):
        return len(self.statements)

    def __hash__(self):
        return self._hash

    @property
    def e(self):
        return self.truth.e

    @property
    def c(self):
        return self.truth.c

    @property
    def f(self):
        return self.truth.f

    def match(self, PTR):
        tmp = self.statements.intersection(PTR.statements)
        self_unmatched = Pattern(self.statements - tmp, self.truth)
        matched = Pattern(tmp, self.truth.revise(PTR.truth))
        PTC_unmatched = Pattern(PTR.statements - tmp, PTR.truth)
        if len(self) > len(PTR):
            return (len(matched) / len(self), self.truth.e), self_unmatched, matched, PTC_unmatched
        elif len(self) < len(PTR):
            return (len(matched) / len(PTR), PTR.truth.e), self_unmatched, matched, PTC_unmatched
        else:
            return (len(matched) / len(self), max(PTR.truth.e, self.truth.e)), self_unmatched, matched, PTC_unmatched


class Pattern_pool:

    def __init__(self, pattern_pool_size):
        self.pattern_pool_size = pattern_pool_size
        self.pattern_pool = []

    def add(self, pattern):  # sorted by e
        tmp = None
        for each in self.pattern_pool:
            if hash(each) == hash(pattern):
                tmp = each
                self.pattern_pool.remove(each)
                break

        if tmp is not None:
            pattern = pattern if pattern.c > tmp.c else tmp

        added = False
        for i in range(len(self.pattern_pool)):
            if pattern.e > self.pattern_pool[i].e:
                self.pattern_pool = self.pattern_pool[:i] + [pattern] + self.pattern_pool[i:]
                added = True
                break

        if not added: self.pattern_pool.append(pattern)

        if len(self.pattern_pool) > self.pattern_pool_size:
            self.pattern_pool.pop(len(self.pattern_pool) // 2)

    def get_PTRs(self, num_PTRs):
        return set(self.pattern_pool[:num_PTRs // 2] + self.pattern_pool[-num_PTRs // 2:])


def match(row_1, row_2, pattern_pool, num_PTRs, just_eval=False):
    PTC = preprocessing_ultimate(row_1, row_2)
    if PTC is None:
        return 0.5
    expectations = []
    for each in pattern_pool.get_PTRs(num_PTRs):
        (sim, e), self_unmatched, matched, PTC_unmatched = PTC.match(each)
        expectations.append(Truth(e, sim))
        if not just_eval:
            pattern_pool.add(self_unmatched)
            pattern_pool.add(matched)
            pattern_pool.add(PTC_unmatched)

    if expectations:
        eva = expectations[0]
        for each in expectations[1:]:
            eva = eva.revise(each)
        return eva.e
    else:
        if not just_eval:
            pattern_pool.add(PTC)
        return 0.5

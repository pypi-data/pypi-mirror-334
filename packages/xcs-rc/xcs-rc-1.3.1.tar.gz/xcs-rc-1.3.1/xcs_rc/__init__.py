# -*- coding: utf-8 -*-
"""
Created on Mon Jul 1 10:13:54 2019
@author: Nugroho Fredivianus
"""

from os import path
from random import choice, choices, randrange

# initial values
cond_init = []
act_init = 0
pred_init = 50.0
prederr_init = 0.0
fit_init = 10.0

default_sep = ","  # default CSV column separator
default_rsep = "|"  # default condition range separator


# Agent class
class Agent:

    def __init__(self, num_actions=2, binaries=False, **kwargs):
        """
        Main XCS instance owned by an agent
        :param num_actions: number of available actions
        :param binaries: using binaries input if True
        :param pressure: the strength for combining ["LOW", "MED", "HIGH"] # stronger means more time required
        :param maxreward: maximal reward given
        :param proreward: projected reward, only used in multi-step cases
        :param maxpopsize: maximal size for the population of rules
        :param tcomb: combining period T_comb
        :param predtol: predicton tolerance, maximum difference allowed to be combined
        :param prederrtol: prediction error tolerance, threshold for hasty detection
        :param nout: attempts to detect outliers if greater than 0
        :param archive: archives combined classifiers and restores when the result is later disproved
        :param autosave: save population every n cycles, default is 0 (inactive)
        :param popfile: default file name to save population to
        :param sep: separator for pop columns, default is ','
        :param rsep: range separator for cond, default is '|'
        """

        # user-defined scenario
        self.num_actions = num_actions
        self.binaries = binaries
        self.maxreward = kwargs.pop("maxreward", 100.0)
        self.proreward = kwargs.pop("proreward", 50.0)

        pressure = kwargs.pop("pressure", "MED")
        self.pressure = "LOW" if pressure.lower() == "low" else "MED" if pressure.lower() == "med" else "HIGH"
        self.nout = kwargs.pop("nout", 0)

        self.autosave = kwargs.pop("autosave", 0)
        self.popfile = kwargs.pop("popfile", "pop.csv")

        # xcs parameters
        self.maxpopsize = kwargs.pop("maxpopsize", 400)
        self.alpha = 0.1
        self.beta = 0.2
        self.gamma = 0.71
        self.delta = 0.1
        self.nu = 1.0
        self.epsilon_0 = 0.01
        self.theta_del = 20
        self.xmax = 0

        # rc parameters
        self.minexp = 1  # minimal experience to be combined
        self.tcomb = kwargs.pop("tcomb", 50)
        self.predtol = kwargs.pop("predtol", 20.0)
        self.prederrtol = kwargs.pop("prederrtol", 10.0)

        # reinforcement cycle
        self.sep = kwargs.pop("sep", default_sep)
        self.rsep = kwargs.pop("rsep", default_rsep)
        self.pop = ClassifierSet(owner=self, name="[Pop]", popfile=self.popfile)  # population
        self.mset = ClassifierSet(owner=self, name="[MatchSet]")  # match set
        self.pa = []  # prediction array
        self.aset = ClassifierSet(owner=self, name="[ActionSet]")  # action set
        self.state = None
        self.reward = 0.0

        self.x = None
        self.y = None
        self.trials = None
        self.cl_counter = None
        self.outliers = None
        self.pop_old = None
        self.filter = None

        self.archive_mode = kwargs.pop("archive", False)
        self.archives = []

        self.reset()

    def reset(self):
        """Reset learning agent."""
        self.pop.empty()
        self.mset.empty()
        self.pa = []
        self.aset.empty()

        self.x = 0
        self.y = 0

        self.trials = 0
        self.cl_counter = 1
        self.outliers = [int(self.nout > 0) - 1]
        self.pop_old = [[-1] for _ in range(self.num_actions)]
        self.filter = []

    def reward_map(self, maxreward=None, projected=None):
        self.maxreward = maxreward if maxreward is not None else self.maxreward
        self.proreward = projected if maxreward is not None else self.proreward

    def build_matchset(self, state, covering=True):
        """
        Build a match set based on the input state.
        Perform covering as a default, in case any actions are not covered by available classifiers.
        :param state: XCS input state
        :param covering: determine whether covering is necessary
        :return: None
        """
        self.state = self.get_input(state)
        self.mset.cl = [cl for cl in self.pop.cl if cl.match(self.state)]
        covered = list(set([cl.act for cl in self.mset.cl]))

        if not covering or len(covered) >= self.num_actions:
            return

        for i in range(self.num_actions):
            if i not in covered:
                self.mset.add(Classifier(
                    cond=floatify(self.state, sep=self.sep, rsep=self.rsep),
                    act=i,
                    pred=self.proreward,
                    owner=self
                ))

    def pick_action_winner(self, pick_method=1):
        """
        Pick an action as a winner based on classifiers existing in match set.
        :param pick_method: 0 = explore, 1 = exploit, 2 = explore_it (set priority to inexperienced classifiers)
        :return: winning action
        """
        pa = []
        exp = []
        inexp = []

        for act in range(self.num_actions):
            tset = [cl for cl in self.mset.cl if cl.act == act]
            pa.append(sum(cl.pred * cl.fit for cl in tset) / sum(cl.fit for cl in tset))
            exp.append(sum(cl.exp for cl in tset))
            inexp.append(len([cl for cl in tset if cl.exp < self.minexp]))

        pa_max = max(pa)
        self.pa = pa

        if max(inexp) > 0 and (pick_method == 0 or (pick_method == 2 and pa_max < self.proreward)):
            maxes = [i for i, v in enumerate(inexp) if v == max(inexp)]
            winner = choice(maxes)

        elif pick_method > 0:  # exploit or explore_it
            if pa.count(pa_max) > 1:
                maxes = [i for i, v in enumerate(pa) if v == pa_max]
                winner = choice(maxes)
            else:
                winner = pa.index(pa_max)

        elif pick_method == 0:  # explore
            winner = choose(pa)[0] if pa_max > 0.0 else randrange(len(pa))

        return winner

    def build_actionset(self, winner, reverse=False):
        """
        Build action set based on the winning action.
        :param winner: winning action
        :param reverse: if True, all actions enter action set except winner
        :return: None
        """
        winner = [winner] if not reverse else [i for i in range(self.num_actions) if i != winner]
        self.aset.cl = [cl for cl in self.mset.cl if cl.act in winner]

        inexp = [cl for cl in self.aset.cl if cl.exp == 0]
        if len(inexp) > 0:
            size = self.pop.size() + len(inexp)
            if size > self.maxpopsize:
                self.del_oversize(size - self.maxpopsize)
            self.pop.add(inexp)

    def apply_reward(self, reward, add_trial=1):
        """
        Apply reward to classifiers in action set.
        :param reward: reward value in integer or float
        :param add_trial: default is 1, setting to 0 means do not consider as a trial (learning cycle)
        :return: list of removed classifiers due to prediction error exceeding tolerance
        """
        if self.aset.size() == 0:
            return []

        self.reward = reward
        cl_del = []
        cl_del_return = []

        for cl in self.aset.cl:
            prev = cl.prederr
            ori_cl = cl.copy()
            cl.exp += 1
            cl.update_prederr(reward)
            cl.update_pred(reward)

            if cl.prederr > self.prederrtol > prev and cl.prederr >= prev and cl.exp > 2 * self.minexp:
                cl_del.append(cl)

        if len(cl_del) > 0:
            self.pop.remove(cl_del)
            self.aset.remove(cl_del)
            cl_del_return.append(ori_cl)

        numsum = sum(cl.num for cl in self.aset.cl)
        for cl in self.aset.cl:
            cl.update_actsetsize(numsum)
        self.aset.update_fitset()
        self.aset.empty()

        self.trials += add_trial
        if self.tcomb > 0 and self.trials % self.tcomb == 0:
            start = 0 if self.pressure != "LOW" else (self.trials // self.tcomb - 1) % self.num_actions
            end = self.num_actions if self.pressure != "LOW" else start + 1

            for act in range(start, end):
                pop_check = sorted([cl.id for cl in self.pop.cl if
                                    cl.act == act and cl.exp >= self.minexp and cl.id not in self.outliers])
                if pop_check != self.pop_old[act]:
                    self.pop.combine_act(act)
                self.pop_old[act] = pop_check

        if self.autosave > 0 and self.trials % self.autosave:
            self.save()

        return cl_del_return

    def next_action(self, state, pick_method=1, force=None, build_aset=True):
        """
        Pick an action after performing an RL cycle
        :param state: XCS input state
        :param pick_method: 0 = explore, 1 = exploit, 2 = explore_it (set priority to inexperienced classifiers)
        :param force: force an action to be picked
        :param build_aset: build an action set, False means learning should be performed
        :return: winning action
        """
        self.build_matchset(state)
        winner = self.pick_action_winner(pick_method) if force is None else force
        if build_aset:
            self.build_actionset(winner)
        return winner

    def one_cycle(self, state, action, reward):
        """
        Perform one RL cycle with the provided [state:action -> reward]
        :param state: XCS input state
        :param action: action to be executed
        :param reward: reward value in integer or float
        :return: number of classifiers in action set
        """
        self.state = self.get_input(state)
        self.mset.cl = [cl for cl in self.pop.cl if cl.match(self.state)]

        covered = list(set([cl.act for cl in self.mset.cl]))
        if action not in covered:
            self.mset.add(Classifier(
                cond=floatify(self.state, sep=self.sep, rsep=self.rsep),
                act=action,
                pred=self.proreward,
                owner=self
            ))

        self.build_actionset(action)
        self.apply_reward(reward)

        return len(self.aset.cl)

    def predict(self, state, action):
        _state = self.get_input(state)
        matches = [cl for cl in self.pop.cl if cl.match(_state) and cl.act == action]
        if len(matches) == 0:
            return pred_init
        return sum(cl.pred * cl.fit for cl in matches) / sum(cl.fit for cl in matches)

    def combine(self):
        """
        Combine population in the set.
        :return: None
        """
        self.pop.combine()

    def del_oversize(self, num_del):
        """
        Perform classifier deletions, e.g., when the size exceeds maximum allowed.
        :param num_del: number of classifiers to be deleted
        :return: None
        """
        inexps = [cl for cl in self.pop.cl if cl.exp == 0]
        if len(inexps) > 0:
            self.pop.remove(inexps)

        if num_del > len(inexps):
            store = [cl for cl in self.mset.cl if cl in self.pop.cl]
            dummy = [cl for cl in self.pop.cl if cl not in store]

            meanfit = sum(cl.fit for cl in dummy) / sum(cl.num for cl in dummy)
            points = [cl.get_delprop(meanfit) for cl in dummy]
            cl_del = [dummy[x] for x in choose(points, num_del - len(inexps))]
            if len(cl_del) > 0:
                for cl in cl_del:
                    if cl not in dummy:
                        continue
                    dummy.remove(cl)
                    del cl

            self.pop.cl = dummy + store

    def get_input(self, vals):
        """
        Modify input if necessary
        :param vals: various types of input value
        :return: input in list, if applicable
        """
        if isinstance(vals, str):
            return self.filter_cond(vals)

        self.binaries = False

        if isinstance(vals, list):
            return vals

        return None

    def load(self, fname: str, empty_first=True, report=True):
        """
        Loads population of classifiers from a file.
        :param fname: file name
        :param empty_first: empty current population before loading
        :param report: print load confirmation if True
        :return: None
        """
        if not path.isfile(fname):
            print(f"File [{fname}] does not exist. Load failed.")
            return False

        with open(fname) as f:
            cls = f.readlines()

        title_line = [i for i, s in enumerate(cls) if s.startswith("id")]
        if len(title_line) == 0:
            title_line.append(0)

        if empty_first:
            self.pop.empty()

        num = 0
        for cl in cls[title_line[-1]:]:
            if cl[0].isdigit():
                z = cl.count(self.sep)
                if self.binaries and z > 8:
                    self.binaries = False

                val = cl.split(self.sep)
                val_cond = self.sep.join(val[i] for i in range(1, z - 6))
                self.pop.add(Classifier(
                    cond=floatify(val_cond, sep=self.sep, rsep=self.rsep),
                    act=int(val[z - 6]), pred=float(val[z - 5]),
                    fit=float(val[z - 4]), prederr=float(val[z - 3]), num=int(val[z - 2]),
                    exp=int(val[z - 1]), actsetsize=int(val[z]),
                    owner=self
                ))
                num += 1

        if report:
            print(f"Loaded to {self.pop.name}: {num} classifiers.")

        return True

    def save(self, fname=None, title="", save_mode='w', sort=None, colnames=None, report=False):
        """
        Save population of classifiers in CSV format
        :param fname: File name
        :param title: Informative title to be saved at the beginning of the file
        :param save_mode: Use 'a' to append or 'w' to rewrite the current file
        :param sort: Sort set before printing, e.g., ["pred", "act"] will sort according to prediction then action
        :param colnames: Optional column names for cond
        :param report: Print report after saving if True
        :return: None
        """
        if fname is None:
            fname = self.popfile

        self.pop.save(
            fname, title=title, save_mode=save_mode, sort=sort,
            colnames=colnames,
            report=report
        )

    def filter_cond(self, cond):
        if len(self.filter) == 0:
            return cond

        for i in reversed(self.filter):
            cond = cond[:i] + cond[:-i - 1]

        return cond

    def collect_restorables(self, cls, combine_id, result=None, visited=None):
        if result is None:
            result = []
        if visited is None:
            visited = set()

        if combine_id in visited:
            return result

        visited.add(combine_id)
        related_cls = [cl for cl in cls if cl.combine_info[1] == combine_id]
        for cl in related_cls:
            if cl.combine_info[0] == 0:
                result.append(cl)

        for cl in related_cls:
            self.collect_restorables(cls, cl.combine_info[0], result, visited)

        return result

    def archive(self, archives):
        if not self.archive_mode:
            return

        _archives = []
        for key, cls in archives.items():
            for cl in cls:
                cl.combine_info[1] = key
            _archives.extend(cls)

        checked = []
        restores = []
        for arc in _archives:
            info = arc.combine_info[0]
            if info not in checked:
                result = self.collect_restorables(self.archives, info)
                self.archives = [cl for cl in result if cl not in result]
                restores.extend(result)
                checked.append(info)

        self.archives.extend(_archives)
        self.pop.add(restores)

    def print_archives(self):
        for cl in self.archives:
            print(cl.to_list())

    def check_feature(self, set_filter=False):
        if not self.binaries:
            return False

        conds = [cl.printable_cond() for cl in self.pop.cl if cl.exp > 0]
        lens = [len(cond) for cond in conds]
        if max(lens) != min(lens):
            return False

        irr = []
        for i in range(1, max(lens) - 1):
            check = [cond[i] for cond in conds]
            hashes = check.count('#')
            if hashes == len(conds):
                irr.append(i - 1)

        if set_filter and len(irr) > 0:
            if len(self.filter) == 0:
                self.filter = irr

            for cl in self.pop.cl:
                for i in reversed(irr):
                    cl.cond = cl.cond[:i] + cl.cond[:-i - 1]

        return irr


class ClassifierSet:
    """ClassifierSet class"""
    def __init__(self, owner=None, name="Set", cls=None, popfile=None):
        if cls is None:
            cls = []
        self.owner = owner
        self.name = name
        self.cl = cls
        self.popfile = popfile
        self.sep = self.owner.sep if owner is not None else default_sep
        self.rsep = self.owner.rsep if owner is not None else default_rsep
        self.combines = 0

    def size(self):
        return len(self.cl)

    def add(self, cls):
        for cl in check_cls(cls):
            self.cl.append(cl)

    def remove(self, cls):
        cl_del = check_cls(cls)
        self.cl = [cl for cl in self.cl if cl not in cl_del]

    def archive(self, archives):
        self.owner.archive(archives)

    def empty(self):
        self.cl = []

    def copy(self):
        return ClassifierSet(name="[Temp]", owner=self.owner, cls=self.cl)

    def exist(self, cl_t):
        return [cl for cl in self.cl if cl.cond == cl_t.cond and cl.act == cl_t.act and cl.pred == cl_t.pred]

    def sort(self, keys=None):  # 0 exp, 1 pred, 2 act, 3 num
        if not keys:
            keys = [1]

        if isinstance(keys, int) or isinstance(keys, str):
            keys = [keys]

        for opt in reversed(keys):
            if opt in [1, "pred"]:
                for cls in self.cl:
                    cls.pred = round(cls.pred, 3)
                self.cl.sort(key=lambda cl: cl.pred, reverse=True)

            elif opt in [2, "act"]:
                self.cl.sort(key=lambda cl: cl.act, reverse=False)

            elif opt in [3, "num"]:
                self.cl.sort(key=lambda cl: cl.num, reverse=True)

            else:
                self.cl.sort(key=lambda cl: cl.exp, reverse=True)

    def update_fitset(self):
        acc = [cl.get_accuracy() for cl in self.cl]
        accsum = sum(ac * cl.num for ac, cl in zip(acc, self.cl))

        for idx, cl in enumerate(self.cl):
            cl.update_fitness(accsum, acc[idx])

    def combine_act(self, act):
        minexp = self.owner.minexp
        predtol = self.owner.predtol
        beta = self.owner.beta

        cset = ClassifierSet(name=f"[C:{act}]")
        cset.cl = [cl for cl in self.cl if cl.act == act]

        if len(cset.cl) < 2:
            return

        local_archive = {}
        pressing = True
        while pressing:
            pressing = False
            cset.sort()
            parent1 = [cl for cl in cset.cl if cl.exp >= minexp]

            for p1 in parent1:
                parent2 = [cl for cl in parent1 if cl != p1 and abs(p1.pred - cl.pred) <= predtol]
                for p2 in parent2:
                    cl_star = Classifier(cond=combine_cond(p1.cond, p2.cond), act=act, owner=self.owner)
                    cl_star.pred = (p1.pred * p1.num + p2.pred * p2.num) / (p1.num + p2.num)

                    disproval = []
                    if (p1.cond != p2.cond or p1.act != p2.act or abs(p1.pred - p2.pred > predtol)) and \
                            not p1.subsumable_to(p2) and not p2.subsumable_to(p1):
                        disproval = [cl for cl in cset.cl if cl.exp > 0 and cl.overlap(cl_star) and not within_range(
                            cl_star.pred, cl.pred, predtol) and cl.id not in self.owner.outliers]

                    if self.owner.outliers[0] == 0 and len(disproval) > 0:
                        for cl in disproval:
                            pa = min(p1.id, p2.id)
                            pb = max(p1.id, p2.id)
                            if [pa, pb] not in cl.disproves:
                                cl.disproves.append([pa, pb])
                            if len(cl.disproves) / cl.exp >= cl.owner.nout:
                                self.owner.outliers.append(cl.id)
                                cl.disproves = []

                    elif len(disproval) == 0:
                        self.combines += 1
                        subsumptions = [cl for cl in cset.cl if cl.subsumable_to(cl_star) and (
                                abs(cl.pred - cl_star.pred) <= predtol or cl.exp == 0)]

                        cl_star.exp = sum(cl.exp for cl in subsumptions)
                        cl_star.num = min(self.owner.maxpopsize, sum(cl.num for cl in subsumptions if cl.exp > 0))
                        cl_star.pred = sum(cl.pred * cl.num for cl in subsumptions if cl.exp > 0) / cl_star.num
                        cl_star.calculate_prederr()
                        cl_star.fit = (fit_init - 1) * pow(1 - beta, cl_star.exp) + 1
                        cl_star.combine_info[0] = self.combines

                        cset.add(cl_star)
                        self.add(cl_star)

                        cset.remove(subsumptions)
                        self.remove(subsumptions)
                        local_archive[self.combines] = subsumptions

                        if self.owner.pressure == "HIGH":
                            pressing = True
                            parent1.clear()
                            parent2.clear()

                        for cl in subsumptions:
                            if self.owner.pressure != "HIGH":
                                if cl in parent1:
                                    parent1.remove(cl)
                            del cl

                        break

        if self.name == "[Pop]" and len(local_archive) > 0:
            self.archive(local_archive)

    def combine(self):
        if self.size() == 0:
            return

        num = max([cl.act for cl in self.cl]) + 1
        for act in range(num):
            self.combine_act(act)

    def get_header(self, colnames=None):
        cols = ["id"]

        if self.owner.binaries:
            cols += ["cond"]

        else:
            condlen = len(self.cl[0].cond)
            cols += ["cond"] if colnames is None else colnames[:condlen]
            cols += [""] * (condlen - len(cols) + 1)

        head = self.sep.join(cols + ["act", "pred", "fit", "prederr", "num", "exp", "actsetsize"])
        return head

    def to_list(self):
        return [cl.to_list() for cl in self.cl]

    def print(self, title="", with_header=True, colnames=None, per_action=False):
        """
        Prints the set to the currently active console
        :param title: Informative title to be saved at the beginning of the file
        :param with_header: Prints the column header
        :param colnames: Optional column names for cond, if with_header is True
        :param per_action: Prints the number of classifiers per action if True
        :return: None
        """
        if per_action:
            acts = [cl.act for cl in self.cl]
            for i in range(self.owner.num_actions):
                print(f"Act {i}: {acts.count(i)}")
            return

        if title != "":
            print(".\n" + title)

        if len(self.cl) > 0:
            if with_header:
                print(self.get_header(colnames=colnames))

            i = 0
            for cl in self.cl:
                i += 1
                print(f"{i}{self.sep}{cl.printable()}")

        else:
            if title != "":
                print("[empty]")

    def save(self, fname=None, title="", save_mode='w', sort=None, colnames=None, report=False):
        """
        Save classifier set in CSV format
        :param fname: File name
        :param title: Informative title to be saved at the beginning of the file
        :param save_mode: Use 'a' to append or 'w' to rewrite the current file
        :param sort: Sort set before printing, e.g., ["pred", "act"] will sort according to prediction then action
        :param colnames: Optional column names for cond
        :param report: Print report after saving if True
        :return: None
        """
        if fname is None:
            if self.popfile is None:
                return

            fname = self.popfile

        if save_mode != 'a':
            save_mode = 'w'

        if sort is None:
            sort = ["pred", "act"]

        try:
            with open(fname, save_mode) as f:
                tset = self.copy()

                if sort is not None and len(tset.cl) > 1:
                    if not isinstance(sort, list):
                        sort = [sort]
                    tset.sort(sort)

                if save_mode == 'a':
                    f.write(".\n")  # vertical self.sep

                if title != "":
                    f.write(title + "\n")

                f.write(tset.get_header(colnames=colnames) + "\n")

                for i, cl in enumerate(tset.cl):
                    f.write(f"{i + 1}{self.sep}{cl.printable()}\n")

            if report:
                print(f"{self.name} stored to {fname}: {tset.size()} classifiers.")

        except Exception as e:
            print("[WARNING] Failed to save population:", e)


class Classifier:
    """Classifier class"""
    def __init__(self, cond=None, act: int = act_init, pred: float = pred_init,
                 fit: float = fit_init, prederr: float = prederr_init, num: int = 1, exp: int = 0,
                 actsetsize: int = 1, owner=None):

        if cond is None:
            cond = cond_init

        number = (int, float, complex)
        new_cond = []
        if cond != cond_init:
            if isinstance(cond, str):
                if not is_binarystr(cond):
                    return

                for c in cond:
                    el = [0.000, 0.000] if c == '0' else [1.000, 1.000]
                    new_cond.append(el)

            elif isinstance(cond, list):
                for c in cond:
                    el = []
                    if isinstance(c, list):
                        if len(c) != 2:
                            print("Cl cond: number of elements error.")
                            return

                        for c2 in c:
                            if not isinstance(c2, number):
                                print("Cl cond: value error.")
                                return

                        el = [min(c), max(c)]

                    elif isinstance(c, number):
                        el = [c, c]

                    new_cond.append(el)

        else:
            new_cond = cond

        self.cond = new_cond
        self.act = act

        self.pred = pred
        self.prederr = prederr
        self.fit = fit
        self.num = num
        self.exp = exp
        self.actsetsize = actsetsize

        self.owner = owner
        self.sep = self.owner.sep if owner is not None else default_sep
        self.rsep = self.owner.rsep if owner is not None else default_rsep

        self.disproves = []
        self.combine_info = [0, 0]
        self.id = owner.cl_counter
        owner.cl_counter += 1

    def match(self, cl):
        if isinstance(cl, Classifier):
            if cl.act != self.act:
                return False
            state = cl.cond
        else:
            state = cl

        if len(state) != len(self.cond):
            return False
        if isinstance(state, str):
            if not is_binarystr(state):
                return False
            state = binarytolist(state)

        for sc, st in zip(self.cond, state):
            if st < sc[0] or st > sc[1]:
                return False

        return True

    def copy(self):
        cl = Classifier(
            cond=self.cond, act=self.act, pred=self.pred,
            prederr=self.prederr, fit=self.fit,
            num=self.num, exp=self.exp, actsetsize=self.actsetsize,
            owner=self.owner
        )
        return cl

    def subsumable_to(self, cl):
        if not isinstance(cl, Classifier) or cl.act != self.act or len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] < cc[0] or sc[1] > cc[1]:
                return False

        return True

    def can_subsume(self, cl):
        if not isinstance(cl, Classifier) or cl.act != self.act or len(cl.cond) != len(self.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if sc[0] > cc[0] or sc[1] < cc[1]:
                return False

        return True

    def resemblance(self, cl):
        if isinstance(cl, Classifier):
            val = cl.cond
        elif isinstance(cl, (str, list)):
            val = floatify(cl, sep=self.sep, rsep=self.rsep)
        else:
            return 0.0

        if len(val) != len(self.cond):
            return 0.0

        res = 0.0
        for sc, cc in zip(self.cond, val):
            if cc[0] == sc[0] or cc[1] == sc[1]:
                add = 0
                if cc[0] == sc[0]:
                    add += 0.5
                if cc[1] == sc[1]:
                    add += 0.5
                if add < 1.0:
                    add += 0.4
                res += add
            elif (cc[0] > sc[0] and cc[1] < sc[1]) or (cc[0] < sc[0] and cc[1] > sc[1]):
                res += 0.8
            elif cc[1] > sc[0] and cc[0] < sc[1]:
                res += 0.7
            else:
                res += 0.4

        return res / len(self.cond)

    def overlap(self, cl):
        if not isinstance(cl, Classifier) or len(self.cond) != len(cl.cond):
            return False

        for sc, cc in zip(self.cond, cl.cond):
            if cc[0] > sc[1] or sc[0] > cc[1]:
                return False

        return True

    def get_delprop(self, meanfit):
        if self.fit / self.num >= self.owner.delta * meanfit or self.exp < self.owner.theta_del:
            return self.actsetsize * self.num
        return self.actsetsize * self.num * meanfit / (self.fit / self.num)

    def update_pred(self, P):
        if self.exp < 1.0 / self.owner.beta:
            self.pred = (self.pred * (float(self.exp) - 1.0) + P) / float(self.exp)
        else:
            self.pred += self.owner.beta * (P - self.pred)

    def update_prederr(self, P):
        if self.exp < 1.0 / self.owner.beta:
            self.prederr = (self.prederr * float(self.exp - 1.0) + abs(P - self.pred)) / self.exp
        else:
            self.prederr += self.owner.beta * (abs(P - self.pred) - self.prederr)

    def get_accuracy(self):
        if self.prederr <= self.owner.epsilon_0:
            return 1.0
        else:
            return self.owner.alpha * pow(self.prederr / self.owner.epsilon_0, -self.owner.nu)

    def update_fitness(self, accsum, accuracy):
        self.fit += self.owner.beta * ((accuracy * self.num) / accsum - self.fit)

    def update_actsetsize(self, numsum):
        if self.exp < 1. / self.owner.beta:
            self.actsetsize = int((self.actsetsize * (self.exp - 1) + numsum) / self.exp)
        else:
            self.actsetsize += int(self.owner.beta * (numsum - self.actsetsize))

    def calculate_prederr(self):
        beta = self.owner.beta
        exp_lim = 1 / beta
        if self.exp <= int(exp_lim):
            self.prederr = abs(self.pred - pred_init) / self.exp
        else:
            self.prederr = (abs(self.pred - pred_init) / exp_lim) * pow(1 - beta, self.exp - int(exp_lim))

    def to_list(self):
        return [
            [[c[0], c[-1]] for c in self.cond], self.act, self.pred,
            self.fit, self.prederr,
            self.num, self.exp, self.actsetsize
        ]

    def printable_cond(self):
        str_cond = ""
        if self.owner.binaries:
            str_cond = '"'
            for sc in self.cond:
                str_cond += "#" if sc[0] != sc[1] else "0" if sc[0] == 0.0 else "1"
            str_cond += '"'

        else:
            for c in self.cond:
                if not isinstance(c, list):
                    str_cond += f"{c:.3f}"
                    continue

                if isinstance(c[0], int) and isinstance(c[1], int):
                    c0 = f"[{c[0]}"
                    c1 = f"{self.rsep}{c[1]}"

                elif c[0].is_integer() and c[1].is_integer():
                    c0 = f"[{int(c[0])}"
                    c1 = f"{self.rsep}{int(c[1])}"

                else:
                    c0 = f"[{c[0]:.3f}"
                    c1 = f"{self.rsep}{c[1]:.3f}"

                str_cond += c0
                if c[0] != c[1]:
                    str_cond += c1
                str_cond += f"]{self.sep}"

            str_cond = str_cond[:-len(self.sep)]

        return str_cond

    def printable(self):
        return self.sep.join([
            self.printable_cond(), f"{self.act}", f"{self.pred:.3f}",
            f"{self.fit:.3f}", f"{self.prederr:.3f}",
            f"{self.num}", f"{self.exp}", f"{self.actsetsize}"
        ])

    def print(self, with_title=False):
        if with_title:
            print("Cond:Act -> Pred | Fit, PredErr, Num, Exp, ActSetSize")
        print(f"{self.printable_cond()}:{self.act} -> {self.pred:.3f} | "
              f"{self.fit:.3f}, {self.prederr:.3f}, {self.num}, {self.exp}, {self.actsetsize}")


# Markov Environment class

class MarkovEnv(object):

    def __init__(self, env='maze4', markov_map=None):
        if markov_map is None:
            markov_map = []
        self.agents = []
        self.map = markov_map

        self.wall = ('O', 'Q')
        self.food = ('F', 'G')
        self.empty = ('*', '.')

        if path.isfile(env):
            with open(env) as f:
                lines = f.readlines()
                for line in lines:
                    self.map.append(line.rstrip('\n'))
        else:
            env = 'maze4'

        if env.lower() == 'maze4':  # average: 3.5 steps
            self.map.append("OOOOOOOO")  # _ _ _ _ _ _ _ _
            self.map.append("O**O**FO")  # _ 5 4 _ 2 1 F _
            self.map.append("OO**O**O")  # _ _ 4 3 _ 1 1 _
            self.map.append("OO*O**OO")  # _ _ 4 _ 2 2 _ _
            self.map.append("O******O")  # _ 5 4 3 3 3 3 _
            self.map.append("OO*O***O")  # _ _ 4 _ 4 4 4 _
            self.map.append("O****O*O")  # _ 5 5 5 5 _ 5 _
            self.map.append("OOOOOOOO")  # _ _ _ _ _ _ _ _

        print("Env initialized:", env)
        for m in self.map:
            print(m)

    def add_agents(self, num, tcomb, xmax, num_actions=8, pressure="HIGH", maxreward=1000.0, proreward=50.0,
                   maxpopsize=400, predtol=50.0, prederrtol=5.0):
        for i in range(num):
            agent = Agent(num_actions=num_actions, binaries=True, pressure=pressure, maxreward=maxreward,
                          maxpopsize=maxpopsize, tcomb=tcomb, predtol=predtol, prederrtol=prederrtol)
            agent.beta = 0.75
            agent.gamma = 0.71
            agent.reward_map(projected=proreward)
            agent.xmax = xmax
            agent.x, agent.y = self.reset_pos()
            self.agents.append(agent)

    def reset_pos(self):
        max_x = len(self.map[0])
        max_y = len(self.map)

        y = -1
        while y < 0 or self.map[y].count('*') + self.map[y].count('.') == 0:
            y = randrange(0, max_y)

        x = -1
        while x < 0 or self.map[y][x] not in self.empty:
            x = randrange(0, max_x)

        return x, y

    def get_state(self, x, y):
        val = ""
        for i in range(8):
            val += decode(self.map[y + add_y(i)][x + add_x(i)])
        return val

    def move(self, x, y, move):
        xx = x + add_x(move)
        yy = y + add_y(move)
        zz = self.map[yy][xx]
        if zz == 'O' or zz == 'Q':
            return x, y, self.map[y][x]
        return xx, yy, zz

    def one_episode(self, pick_method=1):
        agents_steps = []
        for agent in self.agents:
            agent.x, agent.y = self.reset_pos()
            steps = agent.xmax

            for i in range(steps):
                agent.build_matchset(self.get_state(agent.x, agent.y))
                winner = agent.pick_action_winner(pick_method)

                if i > 0:
                    agent.apply_reward(agent.gamma * max(agent.pa))

                agent.build_actionset(winner)
                agent.x, agent.y, agent_now = self.move(agent.x, agent.y, winner)

                if agent_now in self.food:
                    agent.apply_reward(agent.maxreward)
                    steps = i + 1
                    break

            agents_steps.append(steps)

        return agents_steps


def decode(char):
    if not isinstance(char, str):
        return ""
    elif len(char) != 1:
        return ""
    elif char == '*' or char == '.':
        return "000"
    elif char == 'O':
        return "010"
    elif char == 'Q':
        return "011"
    elif char == 'F':
        return "110"
    elif char == 'G':
        return "111"

    return ""


def add_x(move):
    x = 0 if move % 4 == 0 else 1 if move < 4 else -1
    return x


def add_y(move):
    y = -1 if move % 7 < 2 else 0 if move % 4 == 2 else 1
    return y


def is_binarystr(str_cond):
    return len(str_cond.replace("0", "").replace("1", "")) == 0


def binarytolist(val):
    cond = []
    for v in val:
        c = 0.000 if v == '0' else 1.000
        cond.append(c)
    return cond


def floatify(state, sep=",", rsep="|"):
    cond = []
    if isinstance(state, str):
        if state[0] == '[':
            states = state.split(f']{sep}[')
            for s in states:
                s = s.replace('[', '').replace(']', '')
                a = s.split(rsep) if s.count(rsep) == 1 else 2 * [float(s)]
                cond.append([float(a[0]), float(a[1])])
        else:
            if len(state.replace('"', "").replace("0", "").replace("1", "").replace("#", "")) > 0:
                print("Cl cond: not a binary string.")
                return False

            for s in state.replace('"', ''):
                if s == "0":
                    cond.append([0.00, 0.00])
                elif s == "1":
                    cond.append([1.00, 1.00])
                else:
                    cond.append([0.00, 1.00])

    elif isinstance(state, list):
        number = (int, float, complex)
        for s in state:
            if isinstance(s, number):
                cond.append([s, s])
            elif isinstance(s, list):
                cond.append(s)

    return cond


def within_range(val1, val2, tol):
    return val2 + tol >= val1 and val2 <= val1 + tol


def combine_cond(cond1, cond2):
    cond = [[-1.0, -1.0] for _ in range(len(cond1))]
    for i in range(len(cond1)):
        cond[i] = [min(cond1[i][0], cond2[i][0]), max(cond1[i][1], cond2[i][1])]
    return cond


def choose(ar, times=1):
    arr = ar.copy()
    min_arr = min(arr)
    if min_arr < 0:
        arr = [r + min_arr for r in arr]

    if times > len(arr):
        return []

    indices = list(range(len(arr)))
    picks = []
    for i in range(times):
        picked = choices(indices, arr)[0]
        picks.append(picked)
        idx = indices.index(picked)
        indices.pop(idx)
        arr.pop(idx)

    return picks


def check_cls(cls):
    if isinstance(cls, list):
        if len(cls) == 0:
            return []
        for cl in cls:
            if not isinstance(cl, Classifier):
                return []
        return cls
    elif isinstance(cls, Classifier):
        return [cls]
    return []

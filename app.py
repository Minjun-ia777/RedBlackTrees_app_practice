import streamlit as st
import graphviz
import random

# ─────────────────────────────────────────────
#  Red-Black Tree implementation
# ─────────────────────────────────────────────
RED, BLACK = "RED", "BLACK"

class Node:
    def __init__(self, val):
        self.val   = val
        self.color = RED
        self.left  = None
        self.right = None
        self.parent = None

class RBTree:
    def __init__(self):
        self.NIL  = Node(0)
        self.NIL.color = BLACK
        self.root = self.NIL

    def insert(self, val):
        z = Node(val)
        z.left = z.right = z.parent = self.NIL
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z
        self._fix_insert(z)

    def _fix_insert(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def delete(self, val):
        z = self._search(self.root, val)
        if z == self.NIL:
            return False
        self._delete_node(z)
        return True

    def _delete_node(self, z):
        y = z
        y_orig_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_orig_color == BLACK:
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def _transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def _search(self, node, val):
        if node == self.NIL or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def contains(self, val):
        return self._search(self.root, val) != self.NIL

    def black_height(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return 0
        lh = self.black_height(node.left)
        rh = self.black_height(node.right)
        add = 1 if node.color == BLACK else 0
        return add + max(lh, rh)

    def height(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def inorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node != self.NIL:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)
        return result

    def all_nodes(self):
        result = []
        self._collect(self.root, result)
        return result

    def _collect(self, node, result):
        if node != self.NIL:
            self._collect(node.left, result)
            result.append((node.val, node.color))
            self._collect(node.right, result)

    def verify(self):
        """Returns (is_valid, list_of_violations)"""
        violations = []
        if self.root == self.NIL:
            return True, []
        if self.root.color != BLACK:
            violations.append("Rule 2: Root is not black.")
        self._check_red_red(self.root, violations)
        self._check_bh(self.root, violations)
        return len(violations) == 0, violations

    def _check_red_red(self, node, violations):
        if node == self.NIL:
            return
        if node.color == RED:
            if node.left.color == RED:
                violations.append(f"Rule 4: Red node {node.val} has red left child {node.left.val}.")
            if node.right.color == RED:
                violations.append(f"Rule 4: Red node {node.val} has red right child {node.right.val}.")
        self._check_red_red(node.left, violations)
        self._check_red_red(node.right, violations)

    def _bh_at(self, node):
        if node == self.NIL:
            return 0
        l = self._bh_at(node.left)
        r = self._bh_at(node.right)
        if l != r:
            return -1
        add = 1 if node.color == BLACK else 0
        return add + l

    def _check_bh(self, node, violations):
        if node == self.NIL:
            return
        lbh = self._bh_at(node.left)
        rbh = self._bh_at(node.right)
        if lbh != rbh or lbh == -1:
            violations.append(f"Rule 5: Unequal black-heights at node {node.val} (left BH={lbh}, right BH={rbh}).")
        self._check_bh(node.left, violations)
        self._check_bh(node.right, violations)


# ─────────────────────────────────────────────
#  Graphviz renderer
# ─────────────────────────────────────────────
def render_tree(tree, highlight=None):
    dot = graphviz.Digraph(graph_attr={"bgcolor": "transparent", "rankdir": "TB"})
    dot.attr("node", shape="circle", style="filled", fontname="Helvetica", fontsize="14", width="0.55")
    dot.attr("edge", arrowsize="0.6", color="#888888")

    nil_count = [0]

    def add_node(node):
        if node == tree.NIL:
            return
        color   = "#c0392b" if node.color == RED else "#2c2c2a"
        fcolor  = "#ffffff"
        penw    = "2.5" if (highlight and node.val == highlight) else "0"
        pcolor  = "#f1c40f" if (highlight and node.val == highlight) else color
        dot.node(str(node.val),
                 label=str(node.val),
                 fillcolor=color,
                 fontcolor=fcolor,
                 color=pcolor,
                 penwidth=penw)

        if node.left != tree.NIL:
            dot.edge(str(node.val), str(node.left.val))
        else:
            nil_count[0] += 1
            nid = f"nil{nil_count[0]}"
            dot.node(nid, label="∅", fillcolor="#e0e0e0", fontcolor="#888", shape="circle",
                     style="filled", width="0.3", fontsize="10")
            dot.edge(str(node.val), nid, style="dashed", color="#cccccc")

        if node.right != tree.NIL:
            dot.edge(str(node.val), str(node.right.val))
        else:
            nil_count[0] += 1
            nid = f"nil{nil_count[0]}"
            dot.node(nid, label="∅", fillcolor="#e0e0e0", fontcolor="#888", shape="circle",
                     style="filled", width="0.3", fontsize="10")
            dot.edge(str(node.val), nid, style="dashed", color="#cccccc")

        add_node(node.left)
        add_node(node.right)

    if tree.root == tree.NIL:
        dot.node("empty", label="Empty tree", fillcolor="#f5f5f5",
                 fontcolor="#888", shape="rect", style="filled")
    else:
        add_node(tree.root)

    return dot


# ─────────────────────────────────────────────
#  Quiz engine
# ─────────────────────────────────────────────
QUIZ_TYPES = [
    "is_valid",
    "find_bh",
    "find_height",
    "color_of_node",
    "rule_violated",
    "count_black_on_path",
]

def generate_valid_tree(n=6):
    vals = random.sample(range(1, 50), n)
    t = RBTree()
    for v in vals:
        t.insert(v)
    return t, vals

def make_invalid_tree():
    """Build a valid tree then deliberately break one rule."""
    t, vals = generate_valid_tree(5)
    nodes = t.all_nodes()
    if not nodes:
        return t, "rule2"
    mode = random.choice(["rule2", "rule4", "rule5"])
    if mode == "rule2":
        t.root.color = RED
    elif mode == "rule4":
        for val, col in nodes:
            n = t._search(t.root, val)
            if n.color == RED and n.left != t.NIL:
                n.left.color = RED
                break
        else:
            t.root.color = RED
            mode = "rule2"
    elif mode == "rule5":
        leaf_candidates = [(v, c) for v, c in nodes
                           if t._search(t.root, v).left == t.NIL
                           and t._search(t.root, v).right == t.NIL]
        if leaf_candidates:
            v, _ = random.choice(leaf_candidates)
            n = t._search(t.root, v)
            n.color = RED if n.color == BLACK else BLACK
        else:
            t.root.color = RED
            mode = "rule2"
    return t, mode

def make_quiz(qtype):
    """Return (tree, question_str, correct_answer, explanation, highlight_val)"""
    highlight = None

    if qtype == "is_valid":
        if random.random() < 0.5:
            t, _ = generate_valid_tree(random.randint(4, 7))
            answer = "Yes"
            explanation = "All 5 rules are satisfied — root is black, no red-red violations, equal black-heights on all paths."
        else:
            t, mode = make_invalid_tree()
            answer = "No"
            rule_map = {"rule2": "Rule 2 (root must be black)",
                        "rule4": "Rule 4 (red node cannot have red child)",
                        "rule5": "Rule 5 (equal black-height on all paths)"}
            explanation = f"Violated: {rule_map.get(mode, 'a rule')}."
        return t, "Is this a valid Red-Black Tree?", answer, explanation, None

    if qtype == "find_bh":
        t, _ = generate_valid_tree(random.randint(4, 8))
        bh = t.black_height()
        question = "What is the black-height of the root? (Count black nodes root→NULL, not counting NULL)"
        explanation = f"Trace any path from root to NULL counting only black nodes. BH = {bh}."
        return t, question, str(bh), explanation, None

    if qtype == "find_height":
        t, _ = generate_valid_tree(random.randint(4, 8))
        h = t.height()
        question = "What is the total height of the tree? (Number of nodes on the longest root-to-leaf path)"
        explanation = f"The longest path from root to a non-NULL leaf has {h} nodes. Height = {h}."
        return t, question, str(h), explanation, None

    if qtype == "color_of_node":
        t, _ = generate_valid_tree(random.randint(5, 9))
        nodes = t.all_nodes()
        val, color = random.choice(nodes)
        highlight = val
        question = f"What color is node {val}? (type 'red' or 'black')"
        explanation = f"Node {val} is {color.lower()}. You can verify by tracing the insertion path."
        return t, question, color.lower(), explanation, highlight

    if qtype == "rule_violated":
        t, mode = make_invalid_tree()
        rule_map = {"rule2": "2", "rule4": "4", "rule5": "5"}
        answer = rule_map.get(mode, "2")
        question = "This tree violates one rule. Which rule number is violated? (type 2, 4, or 5)"
        rule_desc = {
            "2": "Rule 2 — the root must be black.",
            "4": "Rule 4 — a red node cannot have a red child.",
            "5": "Rule 5 — every path root→NULL must have equal black node count."
        }
        explanation = f"Violated: {rule_desc[answer]}"
        return t, question, answer, explanation, None

    if qtype == "count_black_on_path":
        t, _ = generate_valid_tree(random.randint(4, 8))
        path_nodes = []
        cur = t.root
        while cur != t.NIL:
            path_nodes.append(cur)
            if cur.left != t.NIL:
                cur = cur.left
            else:
                break
        black_count = sum(1 for n in path_nodes if n.color == BLACK)
        path_str = " → ".join(str(n.val) for n in path_nodes) + " → NULL"
        question = f"Count the black nodes on this path (not counting NULL):\n`{path_str}`"
        explanation = f"Black nodes: {[n.val for n in path_nodes if n.color == BLACK]}. Count = {black_count}."
        return t, question, str(black_count), explanation, None

    return generate_valid_tree(), "Placeholder question", "0", "Placeholder explanation", None


# ─────────────────────────────────────────────
#  Streamlit App
# ─────────────────────────────────────────────
st.set_page_config(page_title="RB Tree Practice", page_icon="🌲", layout="wide")

st.markdown("""
<style>
.big-score { font-size: 2.5rem; font-weight: 600; }
.rule-box  { background: #f8f8f8; border-left: 3px solid #c0392b;
             padding: 0.6rem 1rem; border-radius: 4px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ── session state ──
if "tree"        not in st.session_state: st.session_state.tree        = None
if "question"    not in st.session_state: st.session_state.question    = ""
if "answer"      not in st.session_state: st.session_state.answer      = ""
if "explanation" not in st.session_state: st.session_state.explanation = ""
if "highlight"   not in st.session_state: st.session_state.highlight   = None
if "submitted"   not in st.session_state: st.session_state.submitted   = False
if "correct"     not in st.session_state: st.session_state.correct     = False
if "score"       not in st.session_state: st.session_state.score       = 0
if "total"       not in st.session_state: st.session_state.total       = 0
if "qtype"       not in st.session_state: st.session_state.qtype       = None
if "custom_tree" not in st.session_state: st.session_state.custom_tree = RBTree()
if "custom_vals" not in st.session_state: st.session_state.custom_vals = []

# ── sidebar ──
with st.sidebar:
    st.title("🌲 RB Tree Practice")
    st.markdown("---")

    st.markdown("### Rules reference")
    st.markdown("""
<div class="rule-box">
1. Every node is red or black<br>
2. Root is always <b>black</b><br>
3. All NULL leaves are <b>black</b><br>
4. Red node → both children <b>black</b><br>
5. All paths root→NULL have equal <b>black-height</b>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Score")
    st.markdown(f"<div class='big-score'>{st.session_state.score} / {st.session_state.total}</div>",
                unsafe_allow_html=True)
    if st.session_state.total > 0:
        pct = int(100 * st.session_state.score / st.session_state.total)
        st.progress(pct / 100)
        st.caption(f"{pct}% correct")

    if st.button("🔄 Reset score"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()

    st.markdown("---")
    st.markdown("### Question type")
    qtype_labels = {
        "Random":              None,
        "Valid or not?":       "is_valid",
        "Black-height":        "find_bh",
        "Tree height":         "find_height",
        "Color of node":       "color_of_node",
        "Which rule violated": "rule_violated",
        "Count black on path": "count_black_on_path",
    }
    selected_label = st.selectbox("Focus on", list(qtype_labels.keys()))
    st.session_state.qtype = qtype_labels[selected_label]

# ── tabs ──
tab_quiz, tab_explore, tab_verify = st.tabs(["📝 Quiz", "🔬 Explorer", "✅ Verifier"])

# ──────────────────────────────
#  TAB 1 — QUIZ
# ──────────────────────────────
with tab_quiz:
    col_tree, col_quiz = st.columns([3, 2])

    with col_tree:
        st.subheader("Tree")
        if st.session_state.tree is not None:
            dot = render_tree(st.session_state.tree, st.session_state.highlight)
            st.graphviz_chart(dot.source, use_container_width=True)

            nodes = st.session_state.tree.all_nodes()
            if nodes:
                cols = st.columns(min(len(nodes), 8))
                for i, (v, c) in enumerate(sorted(nodes)):
                    color_dot = "🔴" if c == RED else "⚫"
                    cols[i % len(cols)].caption(f"{color_dot} {v}")
        else:
            st.info("Click **New question** to start.")

    with col_quiz:
        st.subheader("Question")
        if st.button("🎲 New question", type="primary", use_container_width=True):
            qtype = st.session_state.qtype or random.choice(QUIZ_TYPES)
            t, q, a, expl, hl = make_quiz(qtype)
            st.session_state.tree        = t
            st.session_state.question    = q
            st.session_state.answer      = a
            st.session_state.explanation = expl
            st.session_state.highlight   = hl
            st.session_state.submitted   = False
            st.rerun()

        if st.session_state.question:
            st.markdown(f"**{st.session_state.question}**")
            st.markdown("")

            if not st.session_state.submitted:
                user_ans = st.text_input("Your answer:", key="user_input",
                                         placeholder="type here...").strip().lower()
                if st.button("✅ Submit", use_container_width=True):
                    correct_ans = st.session_state.answer.strip().lower()
                    st.session_state.correct   = (user_ans == correct_ans)
                    st.session_state.submitted = True
                    st.session_state.total    += 1
                    if st.session_state.correct:
                        st.session_state.score += 1
                    st.rerun()
            else:
                if st.session_state.correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong. Answer: **{st.session_state.answer}**")

                st.markdown("**Explanation:**")
                st.info(st.session_state.explanation)

                if st.button("➡️ Next question", use_container_width=True):
                    qtype = st.session_state.qtype or random.choice(QUIZ_TYPES)
                    t, q, a, expl, hl = make_quiz(qtype)
                    st.session_state.tree        = t
                    st.session_state.question    = q
                    st.session_state.answer      = a
                    st.session_state.explanation = expl
                    st.session_state.highlight   = hl
                    st.session_state.submitted   = False
                    st.rerun()

# ──────────────────────────────
#  TAB 2 — EXPLORER
# ──────────────────────────────
with tab_explore:
    st.subheader("Build your own tree")
    st.caption("Insert and delete values and watch the tree rebalance in real time.")

    col_ctrl, col_vis = st.columns([2, 3])

    with col_ctrl:
        ins_val = st.number_input("Insert value", min_value=1, max_value=99,
                                   value=10, step=1, key="ins")
        if st.button("➕ Insert", use_container_width=True):
            if not st.session_state.custom_tree.contains(ins_val):
                st.session_state.custom_tree.insert(ins_val)
                st.session_state.custom_vals.append(ins_val)
            else:
                st.warning(f"{ins_val} already in tree.")
            st.rerun()

        del_val = st.number_input("Delete value", min_value=1, max_value=99,
                                   value=10, step=1, key="del")
        if st.button("➖ Delete", use_container_width=True):
            ok = st.session_state.custom_tree.delete(del_val)
            if ok:
                if del_val in st.session_state.custom_vals:
                    st.session_state.custom_vals.remove(del_val)
            else:
                st.warning(f"{del_val} not in tree.")
            st.rerun()

        if st.button("🗑️ Clear tree", use_container_width=True):
            st.session_state.custom_tree = RBTree()
            st.session_state.custom_vals = []
            st.rerun()

        st.markdown("---")
        st.markdown("**Quick presets**")
        c1, c2 = st.columns(2)
        if c1.button("From slides\n(7 nodes)"):
            t = RBTree()
            for v in [8, 2, 9, 1, 4, 3, 5]:
                t.insert(v)
            st.session_state.custom_tree = t
            st.session_state.custom_vals = [8, 2, 9, 1, 4, 3, 5]
            st.rerun()
        if c2.button("Random\n(8 nodes)"):
            t = RBTree()
            vals = random.sample(range(1, 50), 8)
            for v in vals:
                t.insert(v)
            st.session_state.custom_tree = t
            st.session_state.custom_vals = vals
            st.rerun()

        st.markdown("---")
        t = st.session_state.custom_tree
        if t.root != t.NIL:
            nodes = t.all_nodes()
            st.markdown("**Stats**")
            st.metric("Nodes", len(nodes))
            st.metric("Height", t.height())
            st.metric("Black-height", t.black_height())
            st.metric("Inorder (sorted)", ", ".join(str(v) for v, _ in sorted(nodes)))

    with col_vis:
        t = st.session_state.custom_tree
        dot = render_tree(t)
        st.graphviz_chart(dot.source, use_container_width=True)

        if t.root != t.NIL:
            is_valid, violations = t.verify()
            if is_valid:
                st.success("✅ Valid Red-Black Tree — all 5 rules satisfied.")
            else:
                st.error("❌ Invalid tree")
                for v in violations:
                    st.warning(v)

# ──────────────────────────────
#  TAB 3 — VERIFIER
# ──────────────────────────────
with tab_verify:
    st.subheader("Verify a tree from your notes")
    st.caption("Enter node values and their colors, and the verifier will check all 5 rules.")

    st.markdown("Enter one node per line in format: `value color parent` — e.g. `10 black none` for the root")

    sample = """10 black none
5 red 10
15 black 10
3 black 5
7 black 5
12 red 15
20 red 15"""

    user_input = st.text_area("Node definitions", value=sample, height=200)

    if st.button("🔍 Verify", type="primary"):
        lines = [l.strip() for l in user_input.strip().splitlines() if l.strip()]
        nodes_map = {}
        errors = []
        root_val = None

        for line in lines:
            parts = line.split()
            if len(parts) != 3:
                errors.append(f"Bad line: `{line}` — expected `value color parent`")
                continue
            try:
                val = int(parts[0])
            except ValueError:
                errors.append(f"Value must be integer: `{parts[0]}`")
                continue
            color = parts[1].upper()
            if color not in ("RED", "BLACK"):
                errors.append(f"Color must be red or black: `{parts[1]}`")
                continue
            parent = parts[2].lower()
            if parent == "none":
                root_val = val
            nodes_map[val] = {"color": color, "parent": parent}

        if errors:
            for e in errors:
                st.error(e)
        else:
            t = RBTree()
            if root_val is not None:
                order = [root_val]
                remaining = [v for v in nodes_map if v != root_val]
                while remaining:
                    added = []
                    for v in remaining:
                        p = nodes_map[v]["parent"]
                        try:
                            pv = int(p)
                            if pv in [x for x in order]:
                                order.append(v)
                                added.append(v)
                        except ValueError:
                            pass
                    if not added:
                        break
                    remaining = [v for v in remaining if v not in added]

                for v in order:
                    t.insert(v)

                for v, info in nodes_map.items():
                    node = t._search(t.root, v)
                    if node != t.NIL:
                        node.color = info["color"]
                if t.root != t.NIL:
                    t.root.color = nodes_map.get(root_val, {}).get("color", "BLACK")

                is_valid, violations = t.verify()
                dot = render_tree(t)
                st.graphviz_chart(dot.source, use_container_width=True)

                if is_valid:
                    st.success("✅ Valid Red-Black Tree — all 5 rules satisfied.")
                else:
                    st.error("❌ This tree violates RB properties:")
                    for v in violations:
                        st.warning(f"• {v}")

                col1, col2, col3 = st.columns(3)
                col1.metric("Nodes", len(nodes_map))
                col2.metric("Height", t.height())
                col3.metric("Black-height", t.black_height())

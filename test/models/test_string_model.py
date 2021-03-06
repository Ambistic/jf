import pytest
from jf.models.stringmodel import StringModel, read_model, _FILENAME_MODELS


def test_load(tmpdir):
    filecontent = """
    [STRINGMODEL1]
    model=salut{name}
    default={"name": 24}
    global_default=12
    escape=$
    sep=_.
    forbidden= ' '
    replace=%%
    """
    with open(tmpdir / _FILENAME_MODELS, "w") as f:
        f.write(filecontent)

    sm = read_model("STRINGMODEL1", tmpdir)
    assert sm.__dict__ == {'model': 'salut{name}', 'default': {'name': 24}, 'global_default': '12',
                           'sep': '_.', 'escape': '$', 'forbidden': ' ', 'replace': '%'}

    print(sm._get_model_slots())


def test_save(tmpdir):
    sm = StringModel(model="hello_not{now}", forbidden=" ")
    sm.save("test", tmpdir)

    with open(tmpdir / "stringmodel.conf", "r") as f:
        content = f.read()

    assert content == '[test]\n' \
                      'model = hello_not{now}\n' \
                      'default = {}\n' \
                      'global_default = \n' \
                      'sep = _.\n' \
                      'escape = $\n' \
                      "forbidden = ' '\n" \
                      'replace = %%\n' \
                      '\n'


def test_extract():
    default = dict(model="triambimutant", end=90, size=8, sample=1, start=49, params="")
    sm = StringModel(
        "expliis_m{model}_e{end}_s{size}_p{params}_n{sample}_t{start}",
        default=default,
        sep="_",
        forbidden=" ",
    )

    params = sm.extract("expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n3_t49")
    assert params == {'end': '90',
         'model': 'triambimutant',
         'params': '-p%smooth%0.6',
         'sample': '3',
         'size': '8',
         'start': '49'
    }


@pytest.fixture
def string_model():
    default = dict(model="triambimutant", end=90, size=8, sample=1, start=49, params="")
    sm = StringModel(
        "expliis_m{model}_e{end}_s{size}_p{params}_n{sample}_t{start}",
        default=default,
        sep="_",
        forbidden=" ",
    )
    return sm


def test_match_ok(string_model):
    assert string_model.match("expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n3_t49")


def test_match_notok(string_model):
    assert not string_model.match("expliis_mtriambimutant_e90_p-p%smooth%0.6_n3_t49")
    # not ok, redo later
    assert not string_model.match("expliis_mtriambimutant_p90_s8_p-p%smooth%0.6_n3_t49")


def test_match_param_ok(string_model):
    assert string_model.match_param("expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n3_t49", dict(start=49))


def test_match_param_notok(string_model):
    assert not string_model.match_param("expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n3_t49", dict(start=48))


def test_pick_last(string_model):
    strings = [
        "expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n3_t49",
        "expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n4_t49",
        "expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n2_t49",
        "expliis_mtriambimutant_e90_s8_p-p%smooth%0.6_n5_t50",
    ]
    last = string_model.pick_last(strings, slot="sample", params=dict(start=49))
    assert last == strings[1]
# 🧠 blue-assistant

🧠 `@assistant` runs AI scripts; DAGs that combine deterministic and AI operations.

```bash
pip install blue-assistant
```

```mermaid
graph LR
    assistant_script_list["@assistant<br>script<br>list"]
    assistant_script_run["@assistant<br>script<br>run -<br>&lt;script&gt;<br>&lt;object-name&gt;"]

    web_crawl["@web<br>crawl -<br>&lt;url-1&gt;+&lt;url-2&gt;<br>&lt;object-name&gt;"]

    web_fetch["@web<br>fetch -<br>&lt;url&gt;<br>&lt;object-name&gt;"]

    script["📜 script"]:::folder
    url["🔗 url"]:::folder
    url2["🔗 url"]:::folder
    url3["🔗 url"]:::folder
    object["📂 object"]:::folder


    script --> assistant_script_list

    script --> assistant_script_run
    object --> assistant_script_run
    assistant_script_run --> object

    url --> web_crawl
    url2 --> web_crawl
    web_crawl --> url3
    web_crawl --> object

    url --> web_fetch
    web_fetch --> object

    bridge_ip["🔗 bridge_ip"]:::folder
    hue_username["🔗 hue_username"]:::folder
    list_of_lights["💡 light IDs"]:::folder

    hue_create_user["@hue<br>create_user"]
    hue_list["@hue<br>list"]
    hue_set["@hue<br>set"]
    hue_test["@hue<br>test"]

    bridge_ip --> hue_create_user
    hue_create_user --> hue_username

    bridge_ip --> hue_list
    hue_username --> hue_list
    hue_list --> list_of_lights

    bridge_ip --> hue_set
    hue_username --> hue_set
    list_of_lights --> hue_set

    bridge_ip --> hue_test
    hue_username --> hue_test
    list_of_lights --> hue_test



    classDef folder fill:#999,stroke:#333,stroke-width:2px;
```

|   |   |
| --- | --- |
| [`orbital-data-explorer`](./blue_assistant/script/repository/orbital_data_explorer) [![image](https://github.com/kamangir/assets/blob/main/blue-assistant/orbital-data-explorer.png?raw=true)](./blue_assistant/script/repository/orbital_data_explorer) Access to the [Orbital Data Explorer](https://ode.rsl.wustl.edu/). 🔥 | [`🌀 blue script`](./blue_assistant/script/) [![image](https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true)](./blue_assistant/script/) A minimal AI DAG interface. |
| [`@hue`](./blue_assistant/script/repository/hue) [![image](https://github.com/kamangir/assets/raw/main/blue-assistant/20250314_143702.jpg?raw=true)](./blue_assistant/script/repository/hue) "send a color command to the Hue LED lights in my apartment." | [`blue-amo`](./blue_assistant/script/repository/blue_amo/README.md) [![image](https://github.com/kamangir/assets/raw/main/blue-amo-2025-02-03-nswnx6/stitching_the_frames-2.png?raw=true)](./blue_assistant/script/repository/blue_amo/README.md) Story development and visualization. |

---

Also home to [`@web`](./blue_assistant/web/)

---


[![pylint](https://github.com/kamangir/blue-assistant/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/blue-assistant/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/blue-assistant/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/blue-assistant/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/blue-assistant.svg)](https://pypi.org/project/blue-assistant/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/blue-assistant)](https://pypistats.org/packages/blue-assistant)

built by 🌀 [`blue_options-4.240.1`](https://github.com/kamangir/awesome-bash-cli), based on 🧠 [`blue_assistant-4.325.1`](https://github.com/kamangir/blue-assistant).

# habitlab-rotation-analysis-cscw2018

## About

Data analysis code for CSCW 2018 paper: "Rotating Online Behavior Change Interventions Increases Effectiveness But Also Increases Attrition"

[Paper: CSCW 2018](https://hci.stanford.edu/publications/2018/habitlab/habitlab-cscw18.pdf)

[ACM DL](https://dl.acm.org/citation.cfm?id=3274364)

[Website](https://habitlab.github.io/)

[Code for system](https://github.com/habitlab)

[Code for data analysis](https://github.com/gkovacs/habitlab-rotation-analysis-cscw2018)

## Abstract

Behavior change systems help people manage their time online. These systems typically consist of a single static intervention, such as a timer or site blocker, to persuade users to behave in ways consistent with their stated goals. However, static interventions decline in effectiveness over time as users begin to ignore them. In this paper, we compare the effectiveness of static interventions to a rotation strategy, where users experience different interventions over time. We built and deployed a browser extension called HabitLab, which features many interventions that the user can enable across social media and other web sites to control their time spent browsing. We ran three in-the-wild field experiments on HabitLab to compare static interventions to rotated interventions. Rotating between interventions increased effectiveness as measured by time on site, but also increased attrition: more users uninstalled HabitLab. To minimize attrition, we introduced a just-in-time information design about rotation. This design reduced attrition rates by half. With this research, we suggest that interaction design, paired with rotation of behavior change interventions, can help users gain control of their online habits.

## Install Prerequisites

```bash
sudo pip install memoize2 lzstring numpy scikit-learn
```

## Run Notebook

```bash
jupyter notebook
```

## License

MIT

## Author

[Geza Kovacs](https://www.gkovacs.com)

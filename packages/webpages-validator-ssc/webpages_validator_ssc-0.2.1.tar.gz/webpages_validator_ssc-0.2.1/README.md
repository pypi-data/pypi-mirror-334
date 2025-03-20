# Simple Site Checker

## (webpages-validator-ssc)

Simple command-line utility for checking links on a web page.

---

## Overview

`simple-site-checker` (`ssc`) is a lightweight Python CLI tool designed to quickly verify the HTTP status codes of all hyperlinks on a given web page. It uses only standard Python libraries and has no external dependencies.

---

## Installation

### Install via PIP

```bash
pip install webpages-validator-ssc
```

```bash
ssc -links -url https://www.example.com
```

### Optional: Save results to CSV

```bash
ssc -links -url https://www.example.com -res results.csv
```

### Optional: set cookies

```bash
ssc -links -url https://www.example.com -auth cookies.txt
```

#### cookies.txt

```txt
name=value
```

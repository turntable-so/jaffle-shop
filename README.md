# 🥪 The Jaffle Shop 🦘

This is a sandbox project for exploring the basic functionality and latest features of dbt. It's based on a fictional restaurant called the Jaffle Shop that serves [jaffles](https://en.wikipedia.org/wiki/Pie_iron).

This README will guide you through setting up the project on dbt Cloud. Working through this example should give you a good sense of how dbt Cloud works and what's involved with setting up your own project. We'll also _optionally_ cover some intermediate topics like setting up Environments and Jobs in dbt Cloud, working with a larger dataset, and setting up pre-commit hooks if you'd like.

> [!NOTE]
> This project is geared towards folks learning dbt Cloud with a cloud warehouse. If you're brand new to dbt, we recommend starting with the [dbt Learn](https://learn.getdbt.com/) platform. It's a free, interactive way to learn dbt, and it's a great way to get started if you're new to the tool. If you just want to try dbt locally as quickly as possible without setting up a data warehouse check out [`jaffle_shop_duckdb`](https://github.com/dbt-labs/jaffle_shop_duckdb).

Ready to go? Grab some water and a nice snack, and let's dig in!

<div>
 <a href="https://www.loom.com/share/a90b383eea594a0ea41e91af394b2811?t=0&sid=da832f06-c08e-43e7-acae-a2a3d8d191bd">
   <p>Welcome to the Jaffle Shop - Watch Intro Video</p>
 </a>
 <a href="https://www.loom.com/share/a90b383eea594a0ea41e91af394b2811?t=0&sid=da832f06-c08e-43e7-acae-a2a3d8d191bd">
   <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/a90b383eea594a0ea41e91af394b2811-with-play.gif">
 </a>
</div>

## Table of contents

1. [Prerequisites](#-prerequisites)
2. [Create new repo from template](#-create-new-repo-from-template)
3. [Platform setup](#%EF%B8%8F-platform-setup)
   1. [dbt Cloud IDE](#%EF%B8%8F-dbt-cloud-ide-most-beginner-friendly)
   2. [dbt Cloud CLI](#-dbt-cloud-cli-if-you-prefer-to-work-locally)
   3. [Load the data](#-load-the-data)
4. [Project setup](#%EF%B8%8F-project-setup)
5. [Going further](#-going-further)
   1. [Setting up dbt Cloud Environments and Jobs](#%EF%B8%8F-setting-up-dbt-cloud-environments-and-jobs)
      1. [Creating an Environment](#-creating-an-environment)
      2. [Creating a Job](#%EF%B8%8F-creating-a-job)
      3. [Explore your DAG](#%EF%B8%8F-explore-your-dag)
   2. [Working with a larger dataset](#-working-with-a-larger-dataset)
      1. [Load the data from S3](#-load-the-data-from-s3)
      2. [Generate via `jafgen` and seed the data with dbt Core](#-generate-via-jafgen-and-seed-the-data-with-dbt-core)
   3. [Pre-commit and SQLFluff](#-pre-commit-and-sqlfluff)

## 💾 Prerequisites

- A dbt Cloud account
- A data warehouse (BigQuery, Snowflake, Redshift, Databricks, or Postgres) with adequate permissions to create a fresh database for this project and run dbt in it
- _Optional_ Python 3.9 or higher (for generating synthetic data with `jafgen`)

## 📓 Create new repo from template

1. <details>
   <summary>Click the green "Use this template" button at the top of the page to create a new repository from this template.</summary>

   ![Click 'Use this template'](/.github/static/use-template.gif)
   </details>

2. Follow the steps to create a new repository. You can choose to only copy the `main` branch for simplicity, or take advantage of the Write-Audit-Publish (WAP) flow we use to maintain the project and copy all branches (which will include `main` and `staging` along with any active feature branches). Either option is fine!

> [!TIP]
> In a setup that follows a WAP flow, you have a `main` branch that serves production data (like downstream dashboards) and is tied to a Production Environment in dbt Cloud, and a `staging` branch that serves a clone of that data and is tied to a Staging Environment in dbt Cloud. You then branch off of `staging` to add new features or fix bugs, and merge back into `staging` when you're done. When you're ready to deploy to production, you merge `staging` into `main`. Staging is meant to be more-or-less a mirror of production, but safe to test breaking changes, so you can verify changes in a production-like environment before deploying them fully. You _write_ to `staging`, _audit_ in `staging`, and _publish_ to `main`.

## 🏗️ Platform setup

1. Create a logical database in your data warehouse for the Jaffle Shop project. We recommend using the name `jaffle_shop` for consistency with the project. This looks different on different platforms (for instance on BigQuery this constitutes creating a new _project_, on Snowflake this is achieved via `create database jaffle_shop;`, and if you're running Postgres locally you can probably skip this). If you're not sure how to do this, we recommend checking out the [Quickstart Guide for your data platform in the dbt Docs](https://docs.getdbt.com/guides).

2. Set up a dbt Cloud account (if you don't have one already, if you do, just create a new project) and follow Step 4 in the [Quickstart Guide for your data platform](https://docs.getdbt.com/guides), to connect your platform to dbt Cloud. Make sure the user you configure for your connections has [adequate database permissions to run dbt](https://docs.getdbt.com/reference/database-permissions/about-database-permissions) in the `jaffle_shop` database.

3. Choose the repo you created in Step 1 of the **Create new repo from template** section as the repository for your dbt Project's codebase.

<img width="500" alt="Repo selection in dbt Cloud" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/daac5bbc-097c-4d57-9628-0c85d348e4a4">

### 🏁 Checkpoint

The following should now be done:

- dbt Cloud connected to your warehouse
- Your copy of this repo set up as the codebase
- dbt Cloud and the codebase pointed at a fresh database or project in your warehouse to work in

You're now ready to start developing with dbt Cloud! Choose a path below (either the [dbt Cloud IDE](<#dbt-cloud-ide-(most-beginner-friendly)>) or the [Cloud CLI](<#dbt-cloud-cli-(if-you-prefer-to-work-locally)>) to get started.

### 😶‍🌫️ dbt Cloud IDE (most beginner friendly)

1. Click `Develop` in the dbt Cloud nav bar. You should be prompted to run a `dbt deps`, which you should do. This will install the dbt packages configured in the `packages.yml` file.

### 💽 dbt Cloud CLI (if you prefer to work locally)

1. Run `git clone [new repo git link]` (or `gh repo clone [repo owner]/[new repo name]` if you prefer GitHub's excellent CLI) to clone your new repo from the first step of the **Create new repo from template** section to your local machine.

2. [Follow the steps on this page](https://cloud.getdbt.com/cloud-cli) to install and set up a dbt Cloud connection with the dbt Cloud CLI.

### 📊 Load the data

There are a few ways to load the data for the project:

- **Using the sample data in the repo**. Add `"jaffle-data"` to the `seed-paths` config in your `dbt_project.yml` as below. This means that when dbt is scanning folders for `seeds` to load it will look in both the `seeds` folder as is default, but _also_ the `jaffle-data` folder which contains a sample of the project data. Seeds are static data files in CSV format that dbt will upload, usually for reference models, like US zip codes mapped to country regions for example, but in this case the feature is hacked to do some data ingestion. This is not what seeds are meant to be used for (dbt is not a data loading tool), but it's useful for this project to give you some data to get going with quickly. Run a `dbt seed` and when it's done either delete the `jaffle-data` folder, remove `jaffle-data` from the `seed-paths` list, or ideally, both.

```yaml dbt_project.yml
seed-paths: ["seeds", "jaffle-data"]
```

```bash
dbt seed
```

- **Load the data via S3**. If you'd prefer a larger dataset (6 years instead of 1), and are working via the dbt Cloud IDE and your platform's web interface, you can also copy the data from a public S3 bucket to your warehouse into a schema called `raw` in your `jaffle_shop` database. [This is discussed here](#-load-the-data-from-s3).

- **Generate a larger dataset on the command line**. If you're working with the dbt Cloud CLI and comfortable with command line basics, you can generate as many years of data as you'd like (up to 10) to load into your warehouse. [This is discussed here](#-generate-via-jafgen-and-seed-the-data-with-dbt-core).

## 👷🏻‍♀️ Project setup

Once your development platform of choice and dependencies are set up, use the following steps to get the project ready for whatever you'd like to do with it.

1. Ensure that you've deleted the `jaffle-data` folder or removed it from the `seed-paths` list in your `dbt_project.yml` (or, ideally, both) if you used the seed method to load the data. This is important, if you don't do this, `dbt build` will re-run the seeds unnecessarily and things will get messy.

2. Run a `dbt build` to build the project.

### 🏁 Checkpoint

The following should now be done:

- Synthetic data loaded into your warehouse
- Development environment set up and ready to go
- The project built and tested

You're free to explore the Jaffle Shop from here, or if you want to learn more about [setting up Environment and Jobs](#%EF%B8%8F-setting-up-dbt-cloud-environments-and-jobs), [generating a larger dataset](#-working-with-a-larger-dataset), or [setting up pre-commit hooks](#-pre-commit-and-sqlfluff) to standardize formatting and linting workflows, carry on!

## 🌅 Going further

> [!NOTE]
> 🐉 Here be dragons! The following sections are for folks who are comfortable with the basics and want to explore more advanced topics. If you're just getting started, it's okay to skip these for now and come back later.

### ☁️ Setting up dbt Cloud Environments and Jobs

#### 🌍 Creating an Environment

dbt Cloud has a powerful abstraction called an Environment. An Environment in dbt Cloud is a _set of configurations_ that dbt uses when it runs your code. It includes things like what version of dbt to use, what schema to build into, credentials to use, and more. You can set up multiple environments in dbt Cloud, and each environment can have its own set of configurations. This is very useful for _running Jobs_. A Job is a set of dbt commands which run in an Environment. Understanding these two concepts is key for getting those most out of dbt Cloud, especially building a robust deployment workflow. Now that we're able to develop in our project, this section will walk you through setting up an Environment and a Job to deploy our project to production.

1. Go to the Deploy tab in the dbt Cloud nav bar and click `Environments`.

2. On the Environment page, click `+ Create Environment`.

   <img width="500" alt="create_environment" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/2fd8039a-8fde-4d7d-84c3-0a30d56fd61f">

3. Name your Environment `Prod` and set it as a `Production` Environment.

   <img width="391" alt="prod_env" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/845d4a31-5a39-4550-944a-ca5bb7b90e55">

4. Fill out the credentials with your warehouse connection details, in real production you'll want to make a Service Account or similar and only give access to the production schema to that user, so that only dbt Cloud Jobs can build into production. For this demo project, it's okay to just use your account credentials.

5. Set the `branch` that this Environment runs on to `main`, then the schema that this Environment builds into to `prod`. This ensures that Jobs configured in this Environment always build into the `prod` schema and run on the `main` branch which we've protected as our production branch.

   <img width="500" alt="custom_branch_main" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/163764c6-bc3c-490b-b262-47e6c71553c9">

6. Click `Save`.

#### 🛠️ Creating a Job

Now we'll create a Job to deploy our project to production. This Job will run the `dbt build` command in the `prod` Environment we just created.

1. Go to the `Prod` Environment you just created.

2. Click `+ Create Job` and choose `Deploy Job` as the Job type.

   <img width="500" alt="create_job" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/9eda2a35-edac-4ad5-b5f4-d273ab3e5351">

3. Name your Job `Production Build`.

4. You can otherwise leave the defaults in place and just click `Save`.

5. Click into your newly created Job and click `Run Now` in the top right corner.

   <img width="500" alt="run_now" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/78cbf863-619a-4213-babe-d26b94363e84">

6. This will kick off a Job to build your project in the `Prod` Environment, which will build into the `prod` schema in your warehouse.

7. Go check out the `prod` schema in your `jaffle_shop` database on your warehouse, you should see the project's models built there!

> [!TIP]
> If you're working in the dbt Cloud IDE, make sure to turn on the 'Defer to staging/production' toggle once you've done this. This will ensure that only modified code is run when you run commands in the IDE, compared against the Production environment you just set up. This will save you significant time and resources!

<img width="500" alt="Screenshot 2024-04-09 at 7 44 36 PM" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/9cdba3b0-6c64-4c40-8380-80c0ec619214">

> [!TIP]
> The dbt Cloud CLI will automatically defer unmodified models to the previously built models in your staging or production environment, so you can run `dbt build`, `dbt test`, etc without worrying about running unnecessary code.

#### 🗺️ Explore your DAG

From here, you should be able to use dbt Explorer (in the `Explore` tab of the dbt Cloud nav bar) to explore your DAG! Explorer is populated with metadata from your designated Production and Staging Environments, so you can see the lineage of your project visually, and much more.

<img width="991" alt="explorer" src="https://github.com/dbt-labs/jaffle-shop/assets/91998347/68b98e29-0e10-461b-80e5-e7665b010c07">

### 🏭 Working with a larger dataset

There are two ways to work with a larger dataset than the default one year of data that comes with the project:

1. **Load the data from S3** which will let you access the canonical 6 year dataset the project is tested against.

2. **Generate via [`jafgen`](https://github.com/dbt-labs/jaffle-shop-generator) and seed the data with dbt Core** which will allow you to generate up to 10 years of data.

#### 💾 Load the data from S3

To load the data from S3, consult the [dbt Documentation's Quickstart Guides](https://docs.getdbt.com/guides) for your data platform to see how to copy data from an S3 bucket to your warehouse. The S3 bucket URIs of the tables you want to copy into your `raw` schema are:

- `raw_customers`: `s3://jaffle-shop-raw/raw_customers.csv`
- `raw_orders`: `s3://jaffle-shop-raw/raw_orders.csv`
- `raw_order_items`: `s3://jaffle-shop-raw/raw_order_items.csv`
- `raw_products`: `s3://jaffle-shop-raw/raw_products.csv`
- `raw_supplies`: `s3://jaffle-shop-raw/raw_supplies.csv`
- `raw_stores`: `s3://jaffle-shop-raw/raw_stores.csv`

#### 🌱 Generate via `jafgen` and seed the data with dbt Core

You'll need to be working on the command line for this option. If you're more comfortable working via web apps, the above method is the path you'll need. [`jafgen`](https://github.com/dbt-labs/jaffle-shop-generator) is a simple tool for generating synthetic Jaffle Shop data that is maintained on a volunteer-basis by dbt Labs employees. This project is more interesting with a larger dataset generated and uploaded to your warehouse. 6 years is a nice amount to fully observe trends like growth, seasonality, and buyer personas that exist in the data. Uploading this amount of data requires a few extra steps, but we'll walk you through them. If you have a preferred way of loading CSVs into your warehouse or an S3 bucket, that will also work just fine, the generated data is just CSV files.

> [!TIP]
> If you'd like to explore further on the command line, but are a little intimidated by the terminal, we've included configuration for a _task runner_ called, fittingly, `task`. It's a simple way to run the commands you need to get started with dbt. You can install it by following the instructions [here](https://taskfile.dev/#/installation). We'll call out the `task` based alternative to each command below that provides an 'easy button'. It's a useful tool to have installed regardless.

1. Create a `profiles.yml` file in the root of your project. This file is already `.gitignore`d so you can keep your credentials safe. If you'd prefer you can instead set up a `profiles.yml` file at the `~/.dbt/profiles.yml` path instead to be extra sure you don't accidentally commit the file.

2. [Add a profile for your warehouse connection in this file](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles#connecting-to-your-warehouse-using-the-command-line) and add this configuration to your `dbt_project.yml` file as a top-level key called `profile` e.g. `profile: my-profile-name`.

> [!IMPORTANT]
> If you do decide to use `task` there is a super-task (`task load`) that will do all of the below steps for you. Just run `task load YEARS=[integer of years to generate] DB=[name of warehouse]` e.g. `task YEARS=4 DB=bigquery` or `task YEARS=7 DB=redshift` etc to perform all the commands necessary to generate and seed the data once your `profiles.yml` file is set up.

3. Create a new virtual environment in your project (I like to call mine `.venv`) and activate it, then install the project's dependencies in it. This will install the `jafgen` tool which you can use to generate the larger datasets. Then install `dbt-core` and your warehouse's adapter. We install dbt Core temporarily because by connecting directly to your warehouse, it can upload larger file sizes than the dbt Cloud server[^1]. You can do this manually or with `task`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install dbt-core dbt-[your warehouse adapter] # e.g. dbt-bigquery
```

**OR**

```bash
task venv
task install DB=[name of warehouse] # e.g. task install DB=bigquery
```

> [!NOTE]
> Because you have an active virtual environment, this new install of `dbt` should take precedence in your [`$PATH`]($PATH`). If you're not familiar with the `PATH` environment variable, just think of this as the order in which your computer looks for commands to run. What's important is that it will look in your active virtual environment first, so when you run `dbt`, it will use the `dbt` you just installed in your virtual environment.

5. Add `jaffle-data` to your `seed-paths` config in your `dbt-project.yml` as [detailed here](#-load-the-data), then run `jafgen` and `seed` the data it generates.

```bash
jafgen [number of years to generate] # e.g. jafgen 6
dbt seed
```

**OR**

```bash
task gen YEARS=[integer of years to generate] # e.g. task gen YEARS=6
task seed
```

6. Remove the `jaffle-data` folder, then uninstall the temporary dbt Core installation. Again, this was to allow you to seed the large data files, you don't need it for the rest of the project which will use the dbt Cloud CLI. You can then delete your `profiles.yml` file and the configuration in your `dbt_project.yml` file. You should also delete the `jaffle-data` path from the `seed-paths` list in your `dbt_project.yml`.

```bash
rm -rf jaffle-data
python3 -m pip uninstall dbt-core dbt-[your warehouse adapter] # e.g. dbt-bigquery
```

**OR**

```bash
task clean
```

You now have a much more interesting and expansive dataset in your `raw` schema to build with! You should now run a `dbt build` to build the project with the new data into your dev schema or trigger your `Production Build` Job in dbt Cloud to build the project in your `prod` schema.

### 🔍 Pre-commit and SQLFluff

There's an optional tool included with the project called `pre-commit`.

[pre-commit](https://pre-commit.com/) automatically runs a suite of of processes on your code, like linters and formatters, when you commit. If it finds an issue and updates a file, you'll need to stage the changes and commit them again (the first commit will not have gone through because pre-commit found and fixed an issue). The outcome of this is that your code will be more consistent automatically, and everybody's changes will be running through the same set of processes. We recommend it for any project.

You can see the configuration for pre-commit in the `.pre-commit-config.yaml` file. It's installed as part of the project's `requirements.txt`, but you'll need to opt-in to using it by running `pre-commit install`. This will install _git hooks_ which run when you commit. You can also run the checks manually with `pre-commit run --all-files` to see what it does without making a commit.

At present the following checks are run:

- `ruff` - an incredibly fast linter and formatter for Python, in case you add any Python models
- `check-yaml` - which validates YAML files
- `end-of-file-fixer` - which ensures all files end with a newline
- `trailing-whitespace` - which trims trailing whitespace from files

At present, the popular SQL linter and formatter SQLFluff doesn't play nicely with the dbt Cloud CLI, so we've omitted it from this project _for now_. We've already built the backend for linting via the Cloud CLI, so this will change very soon! At present if you'd like auto-formatting and linting for SQL, check out the dbt Cloud IDE!

We have kept a `.sqlfluff` config file to show what that looks like, and to future proof the repo for when the Cloud CLI support linting and formatting.

[^1]: Again, I can't emphasize enough that you should not use dbt and seeds for data loading in a production project. This is just for convenience within this learning project.

e7486aada2af7def20d8aca0f468d4b54f7ec337e7d194d9aea75c67a42266a
cd9d1304eddb5ffb3f6a66947c355e45ff69d244a771e658f4a48925212
ecb2e0da1b90a694c788e38c3754fbb725eaff74b68e1715ac31860221aa73d
b753a0e5c17e31ed2d5780ea5cef4e6631ee723268acfbff65d42ab999e58eb
1a44d2e32de5e1ec4c98e5c8d8e57c7c5c0f5c2b6280b1c01f3a4451280bf
ecc2f9a7903dae34bc74de4f6a1da71ae454c84c67b3f46fa1b18e63b68064
bc83495494e1f8a36261b8c03cd680c7134ab28e89a61652f972866e35b117e
c7c268cfb4f5e24a4bfd61ffd4f3d79fd22ac02e2f35efa07879817d8bcb
2fc99f8efeea34a367cf9ff9b91d167e1a884ec3dd065f56c16a95ea111731f
80214df4e1aafd1d2da259b7b6176e01b4cb556f12f95ef24f52ebe824ba
4c93960f3cf45efd674864a8e509baef3fbc8ae20ab13cc768255c5ca19ddeb
29d51bd621e8c6adfb4bbaaa8bf4aea20e434e850abdd798e33b2f2635d23
bdb0d08843d22167b1cc459c6232b1a07b15ee3d46f463b83a882ddf81c32cab
a767f7cb30c12de5bcc2226ca1b4c782bc4ba08a4b52e7d7d46f7cffd5b10ab
eb11d1902be28e32ac5fbbb67d6ecc868a9790494c204539f7428d64b73d210
aef8f645143570773d6adc3c4722968a56a2819e1e94f1bcfa49ba3a687
e658796486485e1db67b46107bcc76ed5cb73f7bbb149df5d86f0f2afbc0
817ca61b8a979f7dfcf42479336d809877eedca957fa5971925bdce95b54635
5cd159d1bbc27cc407621884124354338b58553a13f5b9fa6adc8863940f3
f92a9ca5e3bd3e981f12a071742f51a4e94278ccc19247e926fad28bcf0b1
834cdd8a88b9aec52d344e2cb8cbdeecd5b3ca126ab385dafdd256faf1e
9a848d5454b382a0c1ee4bbaf88fb87982c52d73115463c79978c7947f3398d1
106cc5b5695a47b37197aab7bf556fcd746a453f3661a210db03b5a54ba7c
fabc8b89bff030a8425efeeeed0aad69154cbf4b5b265afec4de8f5fa8ed1d7
426140a986a4b4d82dd2fce69f1f9cae78508b2e532934844dd12e1d85bee724
48ab369fb96a9747a8b725674f25bee9c84aa4b099f44796c8463feb13d53f
3269c397ebb231b6fb99fa55812ea3baa5d7dc5a24b3c7a2897f358cd3c55a9
c28bf8b39df69e1498f9d97e55989992bd19a06516f6c52ff02934bf9f2230
162e806b96db5c92643a83d891b1aba6c45505ab48395e3b684e35b4888acf4
5812e37d3ecbee7b3cc8ff2af8a755c0d1f882df03814aeae7a55bd3d721b
431d20bd7d99bbb5840e6f688a6afe0af6d4438ee784f6976d7ce6d32ec77df
4f9bcd328439fd678530cd1eff2d716dc35d596c331dd466fe753feff7236873
5bc52f2696b7bed0d3ba75191e474efac21ca4914dcd33157b19ee7eeeda7
f37d93b8eb806a32e8a38233ba218a34bb97d66609d5af251cf97a42fbff
1c8a0dbfec3beb2de28f3b2409833319acd2ca56de2364d41dc32878ee72f6
df3e3aae507acfa34e2b3718da9b3240f81c2c14a912c5e7893e8c69616ba48
d195799bfbc4c8cf1dbbdb19132644271860759574e69d5a1a41aa0987c1a8a
69632141dcdd79ba6cc3f357cd1675436c1f6dd588fbbe68f163dfca1b8467
a291c959a7e29323d317bb305fe26579becd5e651349d497bb584854abc
f9b8bee388ec7168d920b61d9d9444bdc1f7fe6aef2ae95bb5bdd8d057e5
954320f2122230ab17e54aa5e560f09ed127ad1257bdf39fe8355eea93e4a1c
ebd9a3f0cacf23cff15718c7fe191ba087df81296ef37aeecb7ecc63dbf54c3
c68a19394a29467b9f5727db9d3c2ab793d3745de4c9464ff79b0b1fa5e6bdb
b0f325c276dd1da9fe563fd2b0344e6220db579b33db7a5642e9f91c52186
c56c3d41c5aecb3f4309e541c7f435abef11844e4366f1b7af405bf6f4caee
24d9148f9e8c7be397924ae1c7c1e6925a471d146571b1f971c9abe556d4
ca8cc545a5c19d94c6374bcaac8f0d25726df8dca879be2a9019c045282b76
655c8b726c82326112882edd89b775aee17a287956d9a494ccbb85a28233de
a5dfa260314bebb78223c821b78a466cae551962f2fea48956f29a5cbb721
eae14bf674a2e69e299a7d0ce73805fce95e3e8a3344baf889e3f79a650136c
77aba88fabf0f4b3e67d46b1a5703019fcd10217a75d251e759295ea64b015
254394f12efcae8c4bf213b5c26dc52e922599104762c2f42c8d5daaa276
e4cfcb176682ed228e7cf6af34a143be84bccf5e24b9a554282b278a820f718
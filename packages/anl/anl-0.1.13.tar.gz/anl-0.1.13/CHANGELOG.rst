Changelog
=========


0.1.13 (2024.03.16)
-------------------

* Compatibility with NegMAS 0.11.2
* Avoid pypi test
* Adding ANLNegotiator to support propose/respond. Negotiators for SAO have the following interface: __call__() which is the default for SAONegotiator. This is implemented by calling propose() and respond() whenever needed. ANL agents implemented __call__ directly. The ANLNegotiator provides an implementation of propose() and respond() assuming __call__ is called directly.
* Renaming old builtin file
* Adding --complete-only/allow-parital to CLI. Controls whether partially run tournaments are considered
* Show debug errors in cli
* Upgrading GitHub Actions to avoid node 16

0.1.11 (2024.04.07)
-------------------

* Adding tournament display and combination  to CLI
* Adding --sort-runs to the CLI
* Passing hidden_time_limit to the Cartesian tournament
* Avoiding plotting issue in windows (not fully tested)
* Requiring latest negmas (v0.10.23)

0.1.10 (2024.04.03)
-------------------

* fixing issue #1 (anlv failure on macOS)
* Correcting git installation method in docs
* requiring negmas 0.10.21
* Better comments on micro
* Defaulting to 3min hidden time limit per negotiation
* pypi workflow update
* Fix tutorial links

0.1.9 (2024.02.14)
------------------

* Adding divide-the-pies scenarios
* Adding workflow to test on negmas master
* Tutorial and docs update
* Update faq

0.1.8 (2023.12.31)
------------------

* bugfix in visualizer initial tournament list
* Correcting auto pushing to PyPi

0.1.7 (2023.12.31)
------------------

* Adding simple dockerfile
* Adding --port, --address to anlv show. You can now set the port and address of the visualizer
* Visualizer parses folders recursively
* minor: faster saving of figs
* Adding mkdocs to dev requirements
* Removing NaiveTitForTat from the default set of competitors
* Improving tutorial

0.1.6 (2023.12.27)
------------------

* Improved visualizer
    - Adding filtering by scenario or strategy to the main view.
    - Adding new options to show scenario statistics, scenario x strategy statistics, and cases with no agreements at all.
    - You can show multiple negotiations together
    - You can show the descriptive statistics of any metric according to strategy or scenario
    - More plotting options for metrics

* Improved CLI
    - Adding the ability to pass parameters to competitors in the CLI.
    - Removing NaiveTitForTat from the default set of competitors
    - Making small tournaments even smaller

* New and improved strategies
    - Adding RVFitter strategy which showcases simple implementation of curve fitting for reserved value estimation and using logging.
    - Adding more comments to NashSeeker strategy
    - Simplified implementation of MiCRO
    - Adding a simple test for MiCRO
    - Avoid failure when Nash cannot be found in NashSeeker

* Migrating to NegMAS 0.10.11. Needed for logging (and 0.10.10 is needed for self.oppponent_ufun)

0.1.5 (2023.12.24)
------------------

* Changing default order of agents
* Adding a basic visualizer
* Adding make-scenarios to the CLI
* Passing opponent ufun in the private info
* Separating implementation of builtin agents
* requiring NegMAS 0.10.9

0.1.4 (2023.12.24)
------------------

* Retrying scenario generation if it failed
* Defaulting to no plotting in windows

0.1.3 (2023.12.23)
------------------

* Defaulting to no-plotting on windows to avoid an error caused by tkinter
* Retry scenario generation on failure. This is useful for piece-wise linear which will fail (by design) if n_pareto happened to be less than n_segments + 1

0.1.2 (2023.12.18)
------------------

* Adding better scenario generation and supporting mixtures of zero-sum, monotonic and general scenarios.
* Requiring negmas 0.10.8

0.1.2 (2023.12.11)
------------------

* Controlling log path in anl2024_tournament() through the added base_path argument

0.1.1 (2023.12.09)
------------------
* Added anl cli for running tournaments.
* Added the ability to hide or show type names during negotiations
* Corrected a bug in importing unique_name
* Now requires negmas 0.10.6

0.1.0 (2023.11.30)
------------------

* Adding ANL 2024 placeholder

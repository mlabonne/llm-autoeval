# LegalBench

### Paper

Title: LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models

Abstract: https://arxiv.org/pdf/2308.11462.pdf

The LegalBench project is an ongoing open science effort to collaboratively curate tasks for evaluating legal reasoning in English large language models (LLMs). The benchmark currently consists of 162 tasks gathered from 40 contributors.

Homepage: https://hazyresearch.stanford.edu/legalbench/

### Citation

```
@misc{guha2023legalbench,
      title={LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models}, 
      author={Neel Guha and Julian Nyarko and Daniel E. Ho and Christopher Ré and Adam Chilton and Aditya Narayana and Alex Chohlas-Wood and Austin Peters and Brandon Waldon and Daniel N. Rockmore and Diego Zambrano and Dmitry Talisman and Enam Hoque and Faiz Surani and Frank Fagan and Galit Sarfaty and Gregory M. Dickinson and Haggai Porat and Jason Hegland and Jessica Wu and Joe Nudell and Joel Niklaus and John Nay and Jonathan H. Choi and Kevin Tobia and Margaret Hagan and Megan Ma and Michael Livermore and Nikon Rasumov-Rahe and Nils Holzenberger and Noam Kolt and Peter Henderson and Sean Rehaag and Sharad Goel and Shang Gao and Spencer Williams and Sunny Gandhi and Tom Zur and Varun Iyer and Zehua Li},
      year={2023},
      eprint={2308.11462},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
@article{koreeda2021contractnli,
  title={ContractNLI: A dataset for document-level natural language inference for contracts},
  author={Koreeda, Yuta and Manning, Christopher D},
  journal={arXiv preprint arXiv:2110.01799},
  year={2021}
}
@article{hendrycks2021cuad,
  title={Cuad: An expert-annotated nlp dataset for legal contract review},
  author={Hendrycks, Dan and Burns, Collin and Chen, Anya and Ball, Spencer},
  journal={arXiv preprint arXiv:2103.06268},
  year={2021}
}
@article{wang2023maud,
  title={MAUD: An Expert-Annotated Legal NLP Dataset for Merger Agreement Understanding},
  author={Wang, Steven H and Scardigli, Antoine and Tang, Leonard and Chen, Wei and Levkin, Dimitry and Chen, Anya and Ball, Spencer and Woodside, Thomas and Zhang, Oliver and Hendrycks, Dan},
  journal={arXiv preprint arXiv:2301.00876},
  year={2023}
}
@inproceedings{wilson2016creation,
  title={The creation and analysis of a website privacy policy corpus},
  author={Wilson, Shomir and Schaub, Florian and Dara, Aswarth Abhilash and Liu, Frederick and Cherivirala, Sushain and Leon, Pedro Giovanni and Andersen, Mads Schaarup and Zimmeck, Sebastian and Sathyendra, Kanthashree Mysore and Russell, N Cameron and others},
  booktitle={Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={1330--1340},
  year={2016}
}
@inproceedings{zheng2021does,
  title={When does pretraining help? assessing self-supervised learning for law and the casehold dataset of 53,000+ legal holdings},
  author={Zheng, Lucia and Guha, Neel and Anderson, Brandon R and Henderson, Peter and Ho, Daniel E},
  booktitle={Proceedings of the eighteenth international conference on artificial intelligence and law},
  pages={159--168},
  year={2021}
}
@article{zimmeck2019maps,
  title={Maps: Scaling privacy compliance analysis to a million apps},
  author={Zimmeck, Sebastian and Story, Peter and Smullen, Daniel and Ravichander, Abhilasha and Wang, Ziqi and Reidenberg, Joel R and Russell, N Cameron and Sadeh, Norman},
  journal={Proc. Priv. Enhancing Tech.},
  volume={2019},
  pages={66},
  year={2019}
}
@article{ravichander2019question,
  title={Question answering for privacy policies: Combining computational and legal perspectives},
  author={Ravichander, Abhilasha and Black, Alan W and Wilson, Shomir and Norton, Thomas and Sadeh, Norman},
  journal={arXiv preprint arXiv:1911.00841},
  year={2019}
}
@article{holzenberger2021factoring,
  title={Factoring statutory reasoning as language understanding challenges},
  author={Holzenberger, Nils and Van Durme, Benjamin},
  journal={arXiv preprint arXiv:2105.07903},
  year={2021}
}
@article{lippi2019claudette,
  title={CLAUDETTE: an automated detector of potentially unfair clauses in online terms of service},
  author={Lippi, Marco and Pa{\l}ka, Przemys{\l}aw and Contissa, Giuseppe and Lagioia, Francesca and Micklitz, Hans-Wolfgang and Sartor, Giovanni and Torroni, Paolo},
  journal={Artificial Intelligence and Law},
  volume={27},
  pages={117--139},
  year={2019},
  publisher={Springer}
}
```

### Groups and Tasks

#### Groups

* `legalbench_exact_match`: The multiple-choices tasks which are evaluated using mean accuracy.
* `legalbench_ISSUE_TASKS`: Issue-spotting tasks in which an LLM must determine if a set of facts raise a particular set of legal questions, implicate an area of the law, or are relevant to a specific party.
* `legalbench_RULE_TASKS`: Rule-recall tasks which require the LLM to generate the correct legal rule on an issue in a jurisdiction (e.g., the rule for hearsay in US federal court), or answer a question about what the law in a jurisdiction does/does not permit.
* `legalbench_CONCLUSION_TASKS`: Rule-conclusion tasks which require an LLM to determine the legal outcome of a set of facts under a specified rule.
* `legalbench_INTERPRETATION_TASKS`: Interpretation tasks which require the LLM to parse and understand a legal text (e.g., classifying contractual clauses).
* `legalbench_RHETORIC_TASKS`: Rhetorical-understanding tasks which require an LLM to reason about legal argumentation and analysis (e.g., identifying textualist arguments).

#### Tasks
* `abercrombie`: Determine the Abercrombie classification for a mark/product pair.
* `canada_tax_court_outcomes`: Classify whether an excerpt from a Canada Tax Court decision includes the outcome of the appeal, and if so, specify whether the appeal was allowed or dismissed.
* `citation_prediction_classification`: Given a legal statement and a case citation, determine if the citation is supportive of the legal statement.
* `consumer_contracts_qa`: Answer yes/no questions on the rights and obligations created by clauses in terms of services agreements.
* `contract_nli_confidentiality_of_agreement`: Identify if the clause provides that the Receiving Party shall not disclose the fact that Agreement was agreed or negotiated.
* `contract_nli_explicit_identification`: Identify if the clause provides that all Confidential Information shall be expressly identified by the Disclosing Party.
* `contract_nli_inclusion_of_verbally_conveyed_information`: Identify if the clause provides that Confidential Information may include verbally conveyed information.
* `contract_nli_limited_use`: Identify if the clause provides that the Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in Agreement.
* `contract_nli_no_licensing`: Identify if the clause provides that the Agreement shall not grant Receiving Party any right to Confidential Information.
* `contract_nli_notice_on_compelled_disclosure`: Identify if the clause provides that the Receiving Party shall notify Disclosing Party in case Receiving Party is required by law, regulation or judicial process to disclose any Confidential Information.
* `contract_nli_permissible_acquirement_of_similar_information`: Identify if the clause provides that the Receiving Party may acquire information similar to Confidential Information from a third party.
* `contract_nli_permissible_copy`: Identify if the clause provides that the Receiving Party may create a copy of some Confidential Information in some circumstances.
* `contract_nli_permissible_development_of_similar_information`: Identify if the clause provides that the Receiving Party may independently develop information similar to Confidential Information.
* `contract_nli_permissible_post-agreement_possession`: Identify if the clause provides that the Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.
* `contract_nli_return_of_confidential_information`: Identify if the clause provides that the Receiving Party shall destroy or return some Confidential Information upon the termination of Agreement.
* `contract_nli_sharing_with_employees`: Identify if the clause provides that the Receiving Party may share some Confidential Information with some of Receiving Party’s employees.
* `contract_nli_sharing_with_third-parties`: Identify if the clause provides that the Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).
* `contract_nli_survival_of_obligations`: Identify if the clause provides that ome obligations of Agreement may survive termination of Agreement.
* `contract_qa`: Answer yes/no questions about whether contractual clauses discuss particular issues.
* `corporate_lobbying`: Predict if a proposed bill is relevant to a company given information about the bill and the company.
* `cuad_affiliate_license-licensee`: Classify if a clause describes a license grant to a licensee (incl. sublicensor) and the affiliates of such licensee/sublicensor.
* `cuad_affiliate_license-licensor`: Classify if the clause describes a license grant by affiliates of the licensor or that includes intellectual property of affiliates of the licensor.
* `cuad_anti-assignment`: Classify if the clause requires consent or notice of a party if the contract is assigned to a third party.
* `cuad_audit_rights`: Classify if the clause gives a party the right to audit the books, records, or physical locations of the counterparty to ensure compliance with the contract.
* `cuad_cap_on_liability`: Classify if the clause specifies a cap on liability upon the breach of a party’s obligation? This includes time limitation for the counterparty to bring claims or maximum amount for recovery.
* `cuad_change_of_control`: Classify if the clause gives one party the right to terminate or is consent or notice required of the counterparty if such party undergoes a change of control, such as a merger, stock sale, transfer of all or substantially all of its assets or business, or assignment by operation of law.
* `cuad_competitive_restriction_exception`: Classify if the clause mentions exceptions or carveouts to Non-Compete, Exclusivity and No-Solicit of Customers.
* `cuad_covenant_not_to_sue`: Classify if the clause specifies that a party is restricted from contesting the validity of the counterparty’s ownership of intellectual property or otherwise bringing a claim against the counterparty for matters unrelated to the contract.
* `cuad_effective_date`: Classify if the clause specifies the date upon which the agreement becomes effective.
* `cuad_exclusivity`: Classify if the clause specifies exclusive dealing commitment with the counterparty. This includes a commitment to procure all “requirements” from one party of certain technology, goods, or services or a prohibition on licensing or selling technology, goods or services to third parties, or a prohibition on collaborating or working with other parties), whether during the contract or after the contract ends (or both).
* `cuad_expiration_date`: Classify if the clause specifies the date upon which the initial term expires.
* `cuad_governing_law`: Classify if the clause specifies which state/country’s law governs the contract.
* `cuad_insurance`: Classify if clause creates a requirement for insurance that must be maintained by one party for the benefit of the counterparty.
* `cuad_ip_ownership_assignment`: Classify if the clause specifies that intellectual property created by one party become the property of the counterparty, either per the terms of the contract or upon the occurrence of certain events.
* `cuad_irrevocable_or_perpetual_license`: Classify if the clause specifies a license grant that is irrevocable or perpetual.
* `cuad_joint_ip_ownership`: Classify if the clause provides for joint or shared ownership of intellectual property between the parties to the contract.
* `cuad_license_grant`: Classify if the clause contains a license granted by one party to its counterparty.
* `cuad_liquidated_damages`: Classify if the clause awards either party liquidated damages for breach or a fee upon the termination of a contract (termination fee).
* `cuad_minimum_commitment`: lassify if the clause specifies a minimum order size or minimum amount or units pertime period that one party must buy from the counterparty.
* `cuad_most_favored_nation`: Does the clause state that if a third party gets better terms on the licensing or sale of technology/goods/services described in the contract, the buyer of such technology/goods/services under the contract shall be entitled to those better terms?
* `cuad_no-solicit_of_customers`: Classify if the clause restricts a party from contracting or soliciting customers or partners of the counterparty, whether during the contract or after the contract ends (or both).
* `cuad_no-solicit_of_employees`: Classify if the clause restricts a party’s soliciting or hiring employees and/or contractors from the counterparty, whether during the contract or after the contract ends (or both).
* `cuad_non-compete`: Classify if the clause restricts the ability of a party to compete with the counterparty or operate in a certain geography or business or technology sector.
* `cuad_non-disparagement`: Classify if the clause requires a party not to disparage the counterparty.
* `cuad_non-transferable_license`: Classify if the clause limits the ability of a party to transfer the license being granted to a third party.
* `cuad_notice_period_to_terminate_renewal`: Classify if the clause specifies a notice period required to terminate renewal.
* `cuad_post-termination_services`: Classify if the clause subjects a party to obligations after the termination or expiration of a contract, including any post-termination transition, payment, transfer of IP, wind-down, last-buy, or similar commitments.
* `cuad_price_restrictions`: Classify if the clause places a restriction on the ability of a party to raise or reduce prices of technology, goods, or services provided.
* `cuad_renewal_term`: Classify if the clause specifies a renewal term.
* `cuad_revenue-profit_sharing`: Classify if the clause require a party to share revenue or profit with the counterparty for any technology, goods, or services.
* `cuad_rofr-rofo-rofn`: Classify if the clause grant one party a right of first refusal, right of first offer or right of first negotiation to purchase, license, market, or distribute equity interest, technology, assets, products or services.
* `cuad_source_code_escrow`: Classify if the clause requires one party to deposit its source code into escrow with a third party, which can be released to the counterparty upon the occurrence of certain events (bankruptcy, insolvency, etc.).
* `cuad_termination_for_convenience`: Classify if the clause specifies that one party can terminate this contract without cause (solely by giving a notice and allowing a waiting period to expire).
* `cuad_third_party_beneficiary`: Classify if the clause specifies that that there a non-contracting party who is a beneficiary to some or all of the clauses in the contract and therefore can enforce its rights against a contracting party.
* `cuad_uncapped_liability`: Classify if the clause specifies that a party’s liability is uncapped upon the breach of its obligation in the contract. This also includes uncap liability for a particular type of breach such as IP infringement or breach of confidentiality obligation.
* `cuad_unlimited-all-you-can-eat-license`: Classify if the clause grants one party an “enterprise,” “all you can eat” or unlimited usage license.
* `cuad_volume_restriction`: Classify if the clause specifies a fee increase or consent requirement, etc. if one party’s use of the product/services exceeds certain threshold.
* `cuad_warranty_duration`: Classify if the clause specifies a duration of any warranty against defects or errors in technology, products, or services provided under the contract.
* `definition_classification`: Given a sentence from a Supreme Court opinion, classify whether or not that sentence offers a definition of a term.
* `diversity_1`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 1).
* `diversity_2`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 2).
* `diversity_3`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 3).
* `diversity_4`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 4).
* `diversity_5`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 5).
* `diversity_6`: Given a set of facts about the citizenships of plaintiffs and defendants and the amounts associated with claims, determine if the criteria for diversity jurisdiction have been met (variant 6).
* `function_of_decision_section`: 1-sentence description of what this particular task does
* `hearsay`: 1-sentence description of what this particular task does
* `insurance_policy_interpretation`: 1-sentence description of what this particular task does
* `international_citizenship_questions`: 1-sentence description of what this particular task does
* `jcrew_blocker`: 1-sentence description of what this particular task does
* `learned_hands_benefits`: 1-sentence description of what this particular task does
* `learned_hands_business`: 1-sentence description of what this particular task does
* `learned_hands_consumer`: 1-sentence description of what this particular task does
* `learned_hands_courts`: 1-sentence description of what this particular task does
* `learned_hands_crime`: 1-sentence description of what this particular task does
* `learned_hands_divorce`: 1-sentence description of what this particular task does
* `learned_hands_domestic_violence`: 1-sentence description of what this particular task does
* `learned_hands_education`: 1-sentence description of what this particular task does
* `learned_hands_employment`: 1-sentence description of what this particular task does
* `learned_hands_estates`: 1-sentence description of what this particular task does
* `learned_hands_family`: 1-sentence description of what this particular task does
* `learned_hands_health`: 1-sentence description of what this particular task does
* `learned_hands_housing`: 1-sentence description of what this particular task does
* `learned_hands_immigration`: 1-sentence description of what this particular task does
* `learned_hands_torts`: 1-sentence description of what this particular task does
* `learned_hands_traffic`: 1-sentence description of what this particular task does
* `legal_reasoning_causality`: 1-sentence description of what this particular task does
* `maud_ability_to_consummate_concept_is_subject_to_mae_carveouts`: 1-sentence description of what this particular task does
* `maud_financial_point_of_view_is_the_sole_consideration`: 1-sentence description of what this particular task does
* `maud_accuracy_of_fundamental_target_rws_bringdown_standard`: 1-sentence description of what this particular task does
* `maud_accuracy_of_target_general_rw_bringdown_timing_answer`: 1-sentence description of what this particular task does
* `maud_accuracy_of_target_capitalization_rw_(outstanding_shares)_bringdown_standard_answer`: 1-sentence description of what this particular task does
* `maud_additional_matching_rights_period_for_modifications_(cor)`: 1-sentence description of what this particular task does
* `maud_application_of_buyer_consent_requirement_(negative_interim_covenant)`: 1-sentence description of what this particular task does
* `maud_buyer_consent_requirement_(ordinary_course)`: 1-sentence description of what this particular task does
* `maud_change_in_law__subject_to_disproportionate_impact_modifier`: 1-sentence description of what this particular task does
* `maud_changes_in_gaap_or_other_accounting_principles__subject_to_disproportionate_impact_modifier`: 1-sentence description of what this particular task does
* `maud_cor_permitted_in_response_to_intervening_event`: 1-sentence description of what this particular task does
* `maud_cor_permitted_with_board_fiduciary_determination_only`: 1-sentence description of what this particular task does
* `maud_cor_standard_(intervening_event)`: 1-sentence description of what this particular task does
* `maud_cor_standard_(superior_offer)`: 1-sentence description of what this particular task does
* `maud_definition_contains_knowledge_requirement_-_answer`: 1-sentence description of what this particular task does
* `maud_definition_includes_asset_deals`: 1-sentence description of what this particular task does
* `maud_definition_includes_stock_deals`: 1-sentence description of what this particular task does
* `maud_fiduciary_exception__board_determination_standard`: 1-sentence description of what this particular task does
* `maud_fiduciary_exception_board_determination_trigger_(no_shop)`: 1-sentence description of what this particular task does
* `maud_fls_(mae)_standard`: 1-sentence description of what this particular task does
* `maud_general_economic_and_financial_conditions_subject_to_disproportionate_impact_modifier`: 1-sentence description of what this particular task does
* `maud_includes_consistent_with_past_practice`: 1-sentence description of what this particular task does
* `maud_initial_matching_rights_period_(cor)`: 1-sentence description of what this particular task does
* `maud_initial_matching_rights_period_(ftr)`: 1-sentence description of what this particular task does
* `maud_intervening_event_-_required_to_occur_after_signing_-_answer`: 1-sentence description of what this particular task does
* `maud_knowledge_definition`: 1-sentence description of what this particular task does
* `maud_liability_standard_for_no-shop_breach_by_target_non-do_representatives`: 1-sentence description of what this particular task does
* `maud_ordinary_course_efforts_standard`: 1-sentence description of what this particular task does
* `maud_pandemic_or_other_public_health_event__subject_to_disproportionate_impact_modifier`: 1-sentence description of what this particular task does
* `maud_pandemic_or_other_public_health_event_specific_reference_to_pandemic-related_governmental_responses_or_measures`: 1-sentence description of what this particular task does
* `maud_relational_language_(mae)_applies_to`: 1-sentence description of what this particular task does
* `maud_specific_performance`: 1-sentence description of what this particular task does
* `maud_tail_period_length`: 1-sentence description of what this particular task does
* `maud_type_of_consideration`: 1-sentence description of what this particular task does
* `nys_judicial_ethics`: 1-sentence description of what this particular task does
* `opp115_data_retention`: 1-sentence description of what this particular task does
* `opp115_data_security`: 1-sentence description of what this particular task does
* `opp115_do_not_track`: 1-sentence description of what this particular task does
* `opp115_first_party_collection_use`: 1-sentence description of what this particular task does
* `opp115_international_and_specific_audiences`: 1-sentence description of what this particular task does
* `opp115_policy_change`: 1-sentence description of what this particular task does
* `opp115_third_party_sharing_collection`: 1-sentence description of what this particular task does
* `opp115_user_access,_edit_and_deletion`: 1-sentence description of what this particular task does
* `opp115_user_choice_control`: 1-sentence description of what this particular task does
* `oral_argument_question_purpose`: 1-sentence description of what this particular task does
* `overruling`: 1-sentence description of what this particular task does
* `personal_jurisdiction`: 1-sentence description of what this particular task does
* `privacy_policy_entailment`: 1-sentence description of what this particular task does
* `privacy_policy_qa`: 1-sentence description of what this particular task does
* `proa`: 1-sentence description of what this particular task does
* `sara_entailment`: 1-sentence description of what this particular task does
* `successor_liability`: 1-sentence description of what this particular task does
* `scalr`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_best_practice_accountability`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_best_practice_audits`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_best_practice_certification`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_best_practice_training`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_best_practice_verification`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_disclosed_accountability`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_disclosed_audits`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_disclosed_certification`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_disclosed_training`: 1-sentence description of what this particular task does
* `supply_chain_disclosure_disclosed_verification`: 1-sentence description of what this particular task does
* `telemarketing_sales_rule`: 1-sentence description of what this particular task does
* `textualism_tool_dictionaries`: 1-sentence description of what this particular task does
* `textualism_tool_plain`: 1-sentence description of what this particular task does
* `ucc_v_common_law`: 1-sentence description of what this particular task does
* `unfair_tos`: 1-sentence description of what this particular task does



### Checklist

For adding novel benchmarks/datasets to the library:
* [ ] Is the task an existing benchmark in the literature?
  * [ ] Have you referenced the original paper that introduced the task?
  * [ ] If yes, does the original paper provide a reference implementation? If so, have you checked against the reference implementation and documented how to run such a test?


If other tasks on this dataset are already supported:
* [ ] Is the "Main" variant of this task clearly denoted?
* [ ] Have you provided a short sentence in a README on what each new variant adds / evaluates?
* [ ] Have you noted which, if any, published evaluation setups are matched by this variant?

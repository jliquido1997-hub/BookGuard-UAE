# ============================================================
# BOOKGUARD UAE
# Automated E-Book Content Screening System
# Version 3.0
# ============================================================

import streamlit as st
import pymupdf
import pandas as pd
import re
from io import BytesIO
from collections import Counter
from pathlib import Path
ICON_PATH = Path(__file__).parent / "bookguard_icon.png"

# ============================================================
# 1. STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BookGuard UAE",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else "📚"
    layout="wide"
)
if ICON_PATH.exists():
    st.image(str(ICON_PATH), width=150)

st.title("BookGuard UAE")
st.subheader("Automated E-Book Content Screening System")

st.info(
    "BookGuard UAE identifies predefined keywords and phrases "
    "in PDF e-books for contextual review by librarians. "
    "Keyword matches do not establish that a book is "
    "inappropriate or non-compliant with UAE regulations."
)

# ============================================================
# 2. KEYWORD PROCESSING FUNCTION
# ============================================================

def make_keywords(text):
    """
    Convert comma-separated text into a list of keywords.
    Remove duplicate entries within each category.
    """
    return list(dict.fromkeys(
        word.strip()
        for word in text.split(",")
        if word.strip()
    ))


# ============================================================
# 3. MASTER KEYWORD DATABASE
# ============================================================

keywords = {

    # CATEGORY 1
    "1. Sexual Content and Nudity": make_keywords("""
    sex, sexual, sexuality, sexualised, sexualized,
    sexualisation, sexualization, naked, nude, nudity,
    breast, breasts, penis, vagina, genitalia, genitals,
    private parts, erotic, erotica, intercourse, orgasm,
    pornography, pornographic, seduction, seductive,
    masturbation, arousal, foreplay, sexual fantasy,
    sexual fantasies, underwear, lingerie, undergarments,
    nakedness, fetish, kink, voyeurism, prostitution,
    prostitute, stripper, strip club, incest, molestation,
    grooming, paedophile, pedophile, paedophilia,
    pedophilia, sexual exploitation, sexual abuse,
    sexual assault, sexual harassment, sex trafficking,
    human trafficking, coercion, explicit content,
    adult content, explicit imagery, intimate touching,
    inappropriate touching, indecent exposure
    """),

    # CATEGORY 2
    "2. Relationships, Romance, Gender and LGBTQ+ Themes": make_keywords("""
    gay, lesbian, bisexual, homosexual, homosexuality,
    LGBTQ, LGBTQ+, LGBT, transgender, transsexual,
    queer, non-binary, nonbinary, gender identity,
    gender expression, gender transition,
    gender reassignment, gender fluid, genderfluid,
    pronouns, same-sex, same sex, same-sex relationship,
    same-sex marriage, boyfriend, girlfriend, kissing,
    kiss, kissed, kisses, intimacy, intimate, affair,
    adultery, romance, romantic, romantic relationship,
    dating, date, crush, love affair, falling in love,
    marriage, married, wedding, divorce, separation,
    homophobia, transphobia, gender discrimination
    """),

    # CATEGORY 3
    # CATEGORY 4
    "4. Christmas, Holidays and Celebrations": make_keywords("""
    Christmas, Xmas, Santa Claus, Santa,
    Father Christmas, Saint Nicholas,
    Christmas tree, Christmas Eve, Christmas Day,
    Christmas present, Christmas gift,
    Christmas stocking, Christmas decorations,
    Christmas carol, carolling, Nativity,
    nativity scene, Jesus, Jesus Christ, Christ,
    crucifix, crucifixion, cross, Easter,
    Easter Bunny, Easter egg, Good Friday,
    Halloween, trick or treat, trick-or-treating,
    witch costume, ghost costume,
    Valentine's Day, Valentine, New Year,
    New Year's Eve, Diwali, Deepavali, Holi,
    Hanukkah, Hannukah, Chanukah, Passover,
    Purim, Yom Kippur, Rosh Hashanah,
    Sabbath, Shabbat, religious holiday,
    religious festival, religious celebration
    """),

    # CATEGORY 5
    "5. Judaism, Jewish Identity, Israel and Regional Political References": make_keywords("""
    Judaism, Jewish, Jew, Jews, Israel, Israeli,
    Jerusalem, Zionism, Zionist, Zionists,
    Talmud, Torah, synagogue, rabbi, rabbis,
    kosher, non-kosher, kippah, yarmulke,
    menorah, Star of David, Hebrew, Holocaust,
    antisemitism, anti-Semitism, Jewish holiday,
    Jewish prayer, Jewish tradition, Jewish law,
    Jewish identity, Jewish culture, Jewish religion,
    Jewish festival, Palestine, Palestinian, Gaza,
    Gaza Strip, Hamas, West Bank, Middle East conflict,
    Israeli-Palestinian conflict, occupation,
    settlement, territorial dispute
    """),

    # CATEGORY 6
    "6. Animals, Pork and Dietary Restrictions": make_keywords("""
    pig, pigs, piglet, piglets, piggy, pigsty,
    pork, bacon, ham, ham sandwich, ham hock,
    pork meat, pork fat, pork chop, pork sausage,
    pork belly, pork ribs, pork roast, lard,
    pigskin, wild boar, boar, swine, sow,
    hog, hogs, gelatin, gelatine, animal fat,
    blood sausage, black pudding, sausage,
    sausages, salami, pepperoni, prosciutto,
    pancetta, chorizo, non-halal, haram, halal,
    kosher food, forbidden food,
    dietary restriction, animal slaughter
    """),

    # CATEGORY 7
    "7. Drugs, Alcohol, Tobacco and Smoking": make_keywords("""
    alcohol, alcoholic, alcohol consumption,
    wine, beer, ale, lager, cider, whiskey,
    whisky, vodka, rum, gin, champagne,
    brandy, tequila, cocktail, liquor, liqueur,
    pub, bar, tavern, brewery, drunk, drunken,
    drunkenness, intoxicated, intoxication,
    intoxicant, intoxicating beverage,
    drinking alcohol, cigarette, cigarettes,
    cigar, cigars, smoking, smoke, smoked,
    smoker, smokers, tobacco, nicotine,
    vape, vaping, e-cigarette, hookah,
    shisha, sisha, sheesha, waterpipe,
    water pipe, pipe smoking, marijuana,
    cannabis, hashish, cocaine, heroin,
    methamphetamine, ecstasy, MDMA, LSD,
    opium, fentanyl, psychedelic, hallucinogen,
    illegal drugs, recreational drugs,
    drug abuse, drug addiction, substance abuse,
    overdose, drug dealer, drug trafficking,
    narcotics, fermentation
    """),

    # CATEGORY 8
    "8. Cannibalism, Body Horror and Disturbing Content": make_keywords("""
    cannibal, cannibals, cannibalism, cannibalistic,
    human flesh, eating human flesh, human sacrifice,
    body parts, severed head, severed limb,
    dismemberment, mutilation, mutilated,
    corpse, corpses, dead body, human remains,
    decomposition, decomposing body, autopsy,
    necrophilia, anthropophagy, organ harvesting,
    body horror, grotesque, gruesome,
    decapitation, disembowelment, rotting flesh,
    skeleton, skull, bones, burial remains
    """),

    # CATEGORY 9
    "9. Diseases, Viruses and Public Health": make_keywords("""
    COVID, COVID-19, coronavirus, SARS-CoV-2,
    pandemic, epidemic, HIV, AIDS, HIV-positive,
    sexually transmitted disease,
    sexually transmitted infection, STD, STI,
    syphilis, gonorrhoea, gonorrhea, chlamydia,
    herpes, hepatitis, tuberculosis, smallpox,
    Ebola, monkeypox, mpox, plague, cholera,
    malaria, measles, infectious disease,
    contagious disease, vaccine, vaccination,
    immunisation, immunization, quarantine,
    isolation, outbreak, virus, viral, bacteria,
    bacterial, infection, infected, disease,
    blood transfusion, organ donation,
    organ transplant
    """),

    # CATEGORY 10
    # CATEGORY 11
    "11. Profanity, Insults and Offensive Language": make_keywords("""
    damn, damned, hell, bloody hell, shit,
    bullshit, fuck, fucking, bitch, bastard,
    asshole, arsehole, crap, slut, whore,
    cunt, dammit, piss, pissed, pissed off,
    motherfucker, dick, dickhead, prick,
    jackass, douchebag, wanker, bollocks,
    bugger, bloody, idiot, stupid, moron,
    dumb, shut up, loser, freak, freakish,
    ugly, fatso, racial profanity, racial slur,
    ethnic slur, derogatory language,
    offensive insult, profanity, swear words,
    swearing, cursing, curse word,
    abusive language
    """),

    # CATEGORY 12
    "12. Political and Ideological Content": make_keywords("""
    communism, communist, fascism, fascist,
    Nazism, Nazi, Hitler, extremist, radical,
    propaganda, revolution, revolutionary,
    rebellion, uprising, anarchy, anarchist,
    discrimination, racism, racist,
    antisemitism, anti-Semitism, Islamophobia,
    white supremacy, nationalism, colonialism,
    imperialism, socialism, capitalism,
    dictatorship, dictator, censorship,
    election, voting, political party,
    political ideology, political extremism,
    racial stereotype, religious discrimination,
    caste system, caste discrimination,
    xenophobia, misogyny, sexism, ableism,
    cultural appropriation, political protest,
    protest, demonstration, government overthrow,
    coup, civil war, political conflict
    """),

    # CATEGORY 13
    # CATEGORY 14
    "14. Pregnancy, Reproduction and Marriage": make_keywords("""
    pregnancy, pregnant, childbirth, labour,
    labor, giving birth, abortion, contraception,
    contraceptive, miscarriage, stillbirth,
    fertility, infertility, IVF,
    in vitro fertilisation, in vitro fertilization,
    birth control, family planning, abortion pill,
    emergency contraception, menstruation,
    menstrual, period, puberty,
    reproductive health, reproductive system,
    breastfeeding, breast milk, surrogacy,
    surrogate mother, adoption, child marriage,
    forced marriage, arranged marriage,
    underage marriage, reproductive rights
    """),

    # CATEGORY 15
    "15. Death, Grief and the Afterlife": make_keywords("""
    death, dying, die, died, dead, dead body,
    deceased, funeral, burial, buried, bury,
    grave, graveyard, cemetery, coffin,
    casket, tomb, tombstone, cremation,
    cremated, ashes, grief, grieving,
    mourning, mourn, bereavement,
    loss of life, afterlife, heaven,
    hellfire, underworld, resurrection,
    reincarnation, ghost, haunting,
    near-death experience, decomposition,
    corpse, human remains, spirit of the dead,
    soul, souls, fatal, fatality, tragedy,
    tragic death, sacrifice
    """),

    # CATEGORY 16
    "16. Gambling and Financial Misconduct": make_keywords("""
    gambling, gamble, gambler, casino,
    betting, bet, wager, lottery, raffle,
    poker, slot machine, jackpot, roulette,
    bingo gambling, riba, usury,
    interest-bearing loan, fraud, fraudulent,
    scam, scamming, bribery, bribe,
    corruption, money laundering,
    embezzlement, insider trading,
    theft, stealing money,
    financial exploitation,
    financial misconduct, illegal betting
    """),

    # CATEGORY 17
    "17. Family, Abuse, Bullying and Social Issues": make_keywords("""
    child abuse, domestic violence, domestic abuse,
    bullying, bully, bullied, harassment,
    exploitation, human trafficking,
    sex trafficking, forced marriage,
    child marriage, honour killing,
    honor killing, blackmail, coercion,
    discrimination, hate speech, stereotype,
    stereotyping, revenge porn, eating disorder,
    anorexia, bulimia, neglect, child neglect,
    abandonment, abandoned child, parental abuse,
    emotional abuse, verbal abuse,
    physical punishment, corporal punishment,
    humiliation, humiliating, mock, mocked,
    mocking, mockery, ridicule, ridiculed,
    teasing, teased, taunting, intimidation,
    victimisation, victimization,
    social exclusion, exclusion, peer pressure,
    cruelty, cruel, prejudice, prejudiced
    """),

    # CATEGORY 18
    "18. Health, Mental Health and Bodily Functions": make_keywords("""
    mental illness, mental health, depression,
    depressed, anxiety, anxious, panic attack,
    psychosis, psychotic, schizophrenia,
    bipolar disorder, eating disorder,
    anorexia, bulimia, obesity, overweight,
    disability, disabled, body image,
    self-esteem, self-harm, suicidal thoughts,
    trauma, traumatic, vomit, vomiting,
    puke, puking, nausea, faeces, feces,
    poo, poop, urine, pee, urination,
    diarrhoea, diarrhea, constipation,
    fart, farting, flatulence,
    toilet humour, toilet humor,
    blood transfusion, infectious disease,
    organ donation, organ harvesting,
    illness, disease, infection, injury,
    wound, wound infection
    """),

    # CATEGORY 19
    "19. Cultural, Racial, Ethnic and Identity Sensitivities": make_keywords("""
    cultural appropriation, religious satire,
    stereotype, stereotyping, sacred object,
    religious clothing, indigenous religion,
    racial stereotype, racial slur, ethnic slur,
    hate speech, homophobia, transphobia,
    misogyny, sexism, ableism, xenophobia,
    caste discrimination, racism, racist,
    prejudice, discrimination, mock, mocked,
    mocking, mockery, ridicule, ridiculed,
    ethnic discrimination, racial discrimination,
    cultural insult, cultural mockery,
    cultural prejudice, minority group,
    tribal stereotype, indigenous stereotype,
    gypsy, gypsies, gipsy, gipsies,
    Romani, Roma, traveller, travelers,
    travellers, nomad, nomadic,
    derogatory ethnic term,
    offensive cultural description
    """),

    # CATEGORY 20
    "20. Additional Sensitive References and Mature Themes": make_keywords("""
    seductive, explicit imagery, adult themes,
    mature themes, inappropriate content,
    sexual references, religious reference,
    political reference, military conflict,
    violence, bloodshed, extremist organisation,
    extremist organization, terrorist organisation,
    terrorist organization, radicalisation,
    radicalization, intoxicating substance,
    cursed object, supernatural power,
    human remains, child exploitation,
    disturbing imagery, frightening scene,
    horror, horror story, nightmare, nightmares,
    terrifying, terror, fear, frightening creature,
    grotesque, gruesome, psychological horror,
    psychological distress, disturbing behaviour,
    disturbing behavior, abusive behaviour,
    abusive behavior, inappropriate relationship,
    controversial subject, sensitive topic
    """),

    # CATEGORY 21
    "21. Additional Fiction, Fairy-Tale and Folklore Screening Terms": make_keywords("""
    fairy, fairies, fairy godmother, fairy tale,
    faerie, faery, elf, elves, goblin, goblins,
    troll, trolls, ogre, ogres, giant, giants,
    dwarf, dwarves, gnome, pixie, sprite,
    leprechaun, dragon, dragons, unicorn,
    mermaid, merman, mythical creature,
    mythical beast, mythical kingdom,
    magical kingdom, enchanted forest,
    enchanted castle, magic mirror,
    wishing well, magic lamp, genie,
    jinn, djinn, djinni, supernatural creature,
    talking animal, shape-shifting, shapeshifter,
    transformation spell, magical transformation,
    cursed princess, sleeping spell,
    magic ring, magic stone, magic crystal,
    mystical creature, mythical hero,
    folklore, folk magic, legend,
    legendary creature, ancient deity,
    underworld, sorcerer's apprentice
    """),

    # CATEGORY 22
    "22. Additional Cultural and Behavioural Screening Terms": make_keywords("""
    disrespect, disrespectful, insult, insulting,
    mock, mocking, mockery, ridicule, blaspheme,
    offensive gesture, rude gesture,
    inappropriate gesture, indecent behaviour,
    indecent behavior, rebellion, rebellious,
    defiance, defiant, disobedience, disobedient,
    disrespecting parents, disrespecting teachers,
    lying, lie, liar, cheating, cheat,
    stealing, theft, dishonesty, deception,
    deceiving, revenge, vengeance, cruelty,
    animal cruelty, animal abuse, animal suffering,
    animal sacrifice, animal killing, hunting,
    poaching, slaughter, blood sport,
    animal fighting, animal experimentation
    """)

}

# ============================================================
# 4. DATABASE STATISTICS
# ============================================================

total_categories = len(keywords)

total_keywords = sum(
    len(words) for words in keywords.values()
)

unique_keywords = len({
    word.casefold()
    for words in keywords.values()
    for word in words
})

# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📚 BookGuard UAE")

    st.write("Master Keyword Database")

    st.metric(
        "Screening Categories",
        total_categories
    )

    st.metric(
        "Keyword Entries",
        total_keywords
    )

    st.metric(
        "Unique Keywords",
        unique_keywords
    )

    st.divider()

    st.write("Screening Settings")

    context_length = st.slider(
        "Context characters",
        min_value=50,
        max_value=500,
        value=150,
        step=50
    )

    selected_categories = st.multiselect(
        "Select Categories",
        options=list(keywords.keys()),
        default=list(keywords.keys())
    )

    st.caption(
        "Select the categories you want to include "
        "in the screening."
    )

# ============================================================
# 6. PDF UPLOAD
# ============================================================

st.header("📄 Upload E-Book")

uploaded_file = st.file_uploader(
    "Select a PDF e-book for content screening",
    type=["pdf"]
)

# ============================================================
# 7. KEYWORD MATCHING FUNCTION
# ============================================================

def create_pattern(keyword):

    parts = keyword.split()

    escaped_parts = [
        re.escape(part)
        for part in parts
    ]

    pattern = (
        r"(?<!\w)"
        + r"\s+".join(escaped_parts)
        + r"(?!\w)"
    )

    return re.compile(
        pattern,
        flags=re.IGNORECASE
    )


# ============================================================
# 8. PDF SCREENING FUNCTION
# ============================================================

def screen_pdf(
    pdf_bytes,
    selected_categories,
    context_length
):

    results = []
    empty_pages = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        total_pages = len(document)

        progress_bar = st.progress(0)

        for page_index in range(total_pages):

            page = document[page_index]

            text = page.get_text(
                "text",
                sort=True
            )

            if not text.strip():

                empty_pages.append(
                    page_index + 1
                )

            for category in selected_categories:

                words = keywords[category]

                for word in words:

                    pattern = create_pattern(word)

                    matches = pattern.finditer(text)

                    for match in matches:

                        start = max(
                            0,
                            match.start() - context_length
                        )

                        end = min(
                            len(text),
                            match.end() + context_length
                        )

                        context = text[start:end]

                        context = re.sub(
                            r"\s+",
                            " ",
                            context
                        ).strip()

                        results.append({

                            "PDF Page": page_index + 1,

                            "Category": category,

                            "Keyword": word,

                            "Matched Text": match.group(),

                            "Context": context,

                            "Review Status": "Pending Review",

                            "Librarian Remarks": ""

                        })

            progress_bar.progress(
                (page_index + 1) / total_pages
            )

    return results, total_pages, empty_pages


# ============================================================
# 9. SCREENING INTERFACE
# ============================================================

if uploaded_file is not None:

    st.success(
        f"File uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Start Content Screening",
        type="primary"
    ):

        if not selected_categories:

            st.warning(
                "Please select at least one category."
            )

        else:

            with st.spinner(
                "Scanning PDF. Please wait..."
            ):

                try:

                    pdf_bytes = uploaded_file.getvalue()

                    results, total_pages, empty_pages = screen_pdf(
                        pdf_bytes,
                        selected_categories,
                        context_length
                    )

                    st.session_state["results"] = results

                    st.session_state["total_pages"] = total_pages

                    st.session_state["empty_pages"] = empty_pages

                    st.session_state["screened_filename"] = (
                        uploaded_file.name
                    )

                except Exception as error:

                    st.error(
                        "The PDF could not be processed. "
                        "Check whether it is valid, encrypted, "
                        "or password-protected."
                    )

                    st.exception(error)

# ============================================================
# 10. SCREENING RESULTS
# ============================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    total_pages = st.session_state["total_pages"]

    empty_pages = st.session_state["empty_pages"]

    st.divider()

    st.header("📊 Screening Dashboard")

    st.success(
        "Content screening completed."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total PDF Pages",
            total_pages
        )

    with col2:

        st.metric(
            "Keyword Matches",
            len(results)
        )

    with col3:

        matched_categories = len({
            result["Category"]
            for result in results
        })

        st.metric(
            "Categories Flagged",
            matched_categories
        )

    with col4:

        matched_pages = len({
            result["PDF Page"]
            for result in results
        })

        st.metric(
            "Pages with Matches",
            matched_pages
        )

    if empty_pages:

        st.warning(
            f"{len(empty_pages)} pages contained "
            "no extractable text. These pages may "
            "require OCR."
        )

    if results:

        df = pd.DataFrame(results)

        # ====================================================
        # 11. CATEGORY SUMMARY
        # ====================================================

        st.subheader(
            "📈 Keyword Matches by Category"
        )

        category_counts = (
            df["Category"]
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Category",
            "Matches"
        ]

        st.bar_chart(
            category_counts.set_index("Category")
        )

        # ====================================================
        # 12. MOST FREQUENT KEYWORDS
        # ====================================================

        st.subheader(
            "🔎 Most Frequently Detected Keywords"
        )

        keyword_counts = (
            df["Keyword"]
            .value_counts()
            .head(20)
            .reset_index()
        )

        keyword_counts.columns = [
            "Keyword",
            "Occurrences"
        ]

        st.dataframe(
            keyword_counts,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # 13. DETAILED RESULTS
        # ====================================================

        st.subheader(
            "📋 Detailed Screening Results"
        )

        filter_category = st.selectbox(
            "Filter by Category",
            ["All Categories"]
            + list(df["Category"].unique())
        )

        if filter_category == "All Categories":

            filtered_df = df.copy()

        else:

            filtered_df = df[
                df["Category"] == filter_category
            ].copy()

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # ====================================================
        # 14. PAGE-BY-PAGE REVIEW
        # ====================================================

        st.subheader(
            "📖 Page-by-Page Content Review"
        )

        pages_with_matches = sorted(
            df["PDF Page"].unique()
        )

        selected_page = st.selectbox(
            "Select PDF Page",
            pages_with_matches
        )

        page_results = df[
            df["PDF Page"] == selected_page
        ]

        for _, row in page_results.iterrows():

            with st.expander(
                f"{row['Keyword']} — {row['Category']}"
            ):

                st.write(
                    "**Detected Keyword:**",
                    row["Keyword"]
                )

                st.write(
                    "**PDF Page:**",
                    row["PDF Page"]
                )

                st.write(
                    "**Context:**"
                )

                st.write(
                    row["Context"]
                )

                st.info(
                    "Review this passage in context. "
                    "A keyword match alone does not "
                    "determine content suitability."
                )

        # ====================================================
        # 15. EXCEL REPORT GENERATION
        # ====================================================

        st.subheader(
            "📥 Download Screening Report"
        )

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            # Detailed findings
            df.to_excel(
                writer,
                index=False,
                sheet_name="Detailed Findings"
            )

            # Category summary
            category_counts.to_excel(
                writer,
                index=False,
                sheet_name="Category Summary"
            )

            # Keyword frequency
            keyword_counts.to_excel(
                writer,
                index=False,
                sheet_name="Keyword Frequency"
            )

            # Screening information
            summary_df = pd.DataFrame({

                "Information": [
                    "File Name",
                    "Total PDF Pages",
                    "Keyword Matches",
                    "Categories Flagged",
                    "Pages with Matches",
                    "Pages Without Extractable Text",
                    "Screening Status"
                ],

                "Value": [
                    st.session_state["screened_filename"],
                    total_pages,
                    len(results),
                    matched_categories,
                    matched_pages,
                    len(empty_pages),
                    "Pending Human Review"
                ]

            })

            summary_df.to_excel(
                writer,
                index=False,
                sheet_name="Screening Summary"
            )

        st.download_button(
            label="📥 Download Complete Excel Report",
            data=output.getvalue(),
            file_name="BookGuard_UAE_Screening_Report.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )

    else:

        st.info(
            "No predefined keywords were detected "
            "in the extractable text. This does not "
            "confirm that the book is suitable or "
            "free from potentially sensitive content."
        )

# ============================================================
# 16. DISCLAIMER
# ============================================================

st.divider()

st.warning(
    "IMPORTANT DISCLAIMER: BookGuard UAE is a "
    "keyword-based screening and review-support tool. "
    "It is not an official UAE regulatory compliance "
    "assessment system. All findings require "
    "contextual human review. References to religion, "
    "identity, disability, health, or other protected "
    "characteristics do not themselves establish "
    "inappropriate content."
)

st.caption(
    "BookGuard UAE | Automated Educational Resource "
    "Content Screening | Version 3.0"
)

# ============================================================
# END OF APPLICATION
# ============================================================

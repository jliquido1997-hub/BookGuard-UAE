import streamlit as st
import pymupdf
import pandas as pd
import re
from io import BytesIO

st.set_page_config(
    page_title="BookGuard UAE",
    page_icon="📚",
    layout="wide"
)

st.title("📚 BookGuard UAE")
st.subheader("Automated E-Book Content Screening System")

st.info(
    "This application identifies predefined keywords "
    "for librarian review. Results do not establish "
    "whether a book complies with UAE regulations."
)

keywords = {
  
def make_keywords(text):
   return list (dict.fromkeys(
        word.strip ()
        for word in text.split (",")
        if word.strip ()
    ))


keywords = {

    # ========================================================
    # 1. SEXUAL CONTENT AND NUDITY
    # ========================================================

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


    # ========================================================
    # 2. RELATIONSHIPS, ROMANCE, GENDER AND LGBTQ+ THEMES
    # ========================================================

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


    # ========================================================
    # 3. RELIGION AND RELIGIOUS SENSITIVITY
    # ========================================================

    "3. Religion and Religious Sensitivity": make_keywords("""
    Allah, God, gods, goddess, deity, divine, Quran,
    Qur'an, Koran, Islam, Islamic, Muslim,
    Prophet Muhammad, prophet, prophecy, prayer,
    pray, praying, worship, worshipping, scripture,
    sacred, holy, holiness, blessing, blessed,
    blasphemy, blasphemous, atheist, atheism,
    apostasy, heresy, sacrilege, idolatry, idol,
    religious conversion, religious criticism,
    religious satire, religious insult,
    religious discrimination, religious symbol,
    religious clothing, religious ceremony,
    religious ritual, proselytising, proselytizing,
    polytheism, monotheism, temple, mosque,
    church, chapel, cathedral, shrine, monastery,
    altar, priest, pastor, minister, monk, nun,
    rabbi, imam, preacher, sermon, chanting,
    chant, chanted, hymn, hymns, miracle, omen,
    evil, devil, Satan, satanic, demon, witchcraft,
    occult, paganism, pagan, Christianity,
    Christian, Catholic, Protestant, Bible,
    New Testament, Old Testament, Hinduism,
    Hindu, Buddhism, Buddhist, Sikhism, Sikh,
    Jainism, Jain, Mormon, Jehovah's Witness,
    sectarianism, religious extremism, mock,
    mocked, mocking, mockery, ridicule,
    religious mockery
    """),


    # ========================================================
    # 4. CHRISTMAS, HOLIDAYS AND CELEBRATIONS
    # ========================================================

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


    # ========================================================
    # 5. JUDAISM, JEWISH IDENTITY, ISRAEL AND REGIONAL POLITICS
    # ========================================================

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


    # ========================================================
    # 6. ANIMALS, PORK AND DIETARY RESTRICTIONS
    # ========================================================

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


    # ========================================================
    # 7. DRUGS, ALCOHOL, TOBACCO AND SMOKING
    # ========================================================

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


    # ========================================================
    # 8. CANNIBALISM, BODY HORROR AND DISTURBING CONTENT
    # ========================================================

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


    # ========================================================
    # 9. DISEASES, VIRUSES AND PUBLIC HEALTH
    # ========================================================

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


    # ========================================================
    # 10. VIOLENCE, WEAPONS, WAR AND CRIME
    # ========================================================

    "10. Violence, Weapons, War and Crime": make_keywords("""
    murder, murderer, murdered, kill, killed,
    killer, killing, blood, bloody, bloodshed,
    gore, gory, torture, tortured, rape,
    sexual assault, abuse, physical abuse,
    suicide, suicidal, self-harm, cutting,
    gun, pistol, rifle, shotgun, firearm,
    bullet, ammunition, knife, dagger, sword,
    blade, stabbing, stabbed, shooting, shot,
    bomb, bombing, explosion, explosive,
    terrorism, terrorist, extremism,
    radicalisation, radicalization, war,
    warfare, battle, battlefield, military,
    soldier, combat, fighting, fight,
    attack, attacked, assault, violence,
    violent, landmine, grenade, missile,
    chemical weapon, biological weapon,
    nuclear weapon, genocide, war crime,
    hostage, kidnapping, abducted, abduction,
    execution, assassination, strangulation,
    beating, domestic abuse, child exploitation,
    coercion, threat, threatening, blackmail,
    harassment, honour killing, honor killing,
    massacre, slaughter, mutilation, revenge,
    revenge killing, poison, poisoned, poisoning,
    drowning, suffocation, imprisonment,
    prison, jail, criminal, crime, theft,
    robbery, stealing, burglar, burglary,
    vandalism
    """),


    # ========================================================
    # 11. PROFANITY, INSULTS AND OFFENSIVE LANGUAGE
    # ========================================================

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


    # ========================================================
    # 12. POLITICAL AND IDEOLOGICAL CONTENT
    # ========================================================

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


    # ========================================================
    # 13. OCCULT, PARANORMAL AND SUPERNATURAL THEMES
    # ========================================================

    "13. Occult, Paranormal, Fortune-Telling and Supernatural Themes": make_keywords("""
    spell, spells, spellbook, spellcasting,
    witch, witches, witchcraft, wizard, wizardry,
    warlock, sorcerer, sorceress, sorcery,
    magician, magic, magical, enchantment,
    enchanted, enchantress, charm, charms,
    potion, potions, magic wand, wand,
    broomstick, demon, demonic, devil,
    Satan, satanic, evil, evil spirit,
    evil eye, evil force, dark force,
    dark magic, summoning, summon,
    ritual, rituals, chanting, chant,
    chanted, incantation, incantations,
    necromancy, exorcism, possession,
    possessed, voodoo, hoodoo, black magic,
    white magic, dark arts, occult, occultism,
    fortune teller, fortune-teller,
    fortune telling, fortune-telling,
    fortuneteller, psychic, psychic reading,
    palm reading, palmistry, tarot,
    tarot cards, crystal ball, divination,
    soothsayer, seer, clairvoyant, medium,
    mediumship, séance, seance, channeling,
    channelling, astrology, astrologer,
    horoscope, zodiac, star sign, omen,
    omens, prophecy, prophecy reading,
    prediction, supernatural, paranormal,
    supernatural power, supernatural being,
    supernatural creature, spirit, spirits,
    spirit world, ghost, ghosts, ghostly,
    haunted, haunting, haunt, phantom,
    apparition, poltergeist, spectre,
    specter, banshee, vampire, werewolf,
    zombie, undead, monster, monstrous,
    curse, cursed, curses, hex, hexed,
    jinx, jinxed, superstition, superstitious,
    talisman, amulet, mystical, mysticism,
    mythology, mythological god, goddess,
    afterlife, reincarnation, resurrection,
    near-death experience
    """),


    # ========================================================
    # 14. PREGNANCY, REPRODUCTION AND MARRIAGE
    # ========================================================

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


    # ========================================================
    # 15. DEATH, GRIEF AND THE AFTERLIFE
    # ========================================================

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


    # ========================================================
    # 16. GAMBLING AND FINANCIAL MISCONDUCT
    # ========================================================

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


    # ========================================================
    # 17. FAMILY, ABUSE, BULLYING AND SOCIAL ISSUES
    # ========================================================

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


    # ========================================================
    # 18. HEALTH, MENTAL HEALTH AND BODILY FUNCTIONS
    # ========================================================

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


    # ========================================================
    # 19. CULTURAL, RACIAL, ETHNIC AND IDENTITY SENSITIVITIES
    # ========================================================

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


    # ========================================================
    # 20. ADDITIONAL SENSITIVE REFERENCES AND MATURE THEMES
    # ========================================================

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


    # ========================================================
    # 21. FICTION, FAIRY-TALE AND FOLKLORE SCREENING TERMS
    # ========================================================

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


    # ========================================================
    # 22. CULTURAL AND BEHAVIOURAL SCREENING TERMS
    # ========================================================

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
# DATABASE VALIDATION
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

print("BOOKGUARD UAE MASTER KEYWORD DATABASE")
print("-----------------------------------")
print("Screening categories:", total_categories)
print("Total category keyword entries:", total_keywords)
print("Unique keywords and phrases:", unique_keywords)
print("Database loaded successfully!")
}

uploaded_file = st.file_uploader(
    "Upload an E-Book (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Start Content Screening"):

        results = []
        pages_without_text = []

        with st.spinner("Scanning PDF..."):

            try:
                pdf_bytes = uploaded_file.getvalue()

                with pymupdf.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                ) as document:

                    total_pages = len(document)

                    for page_index in range(total_pages):

                        page = document[page_index]
                        text = page.get_text()

                        if not text.strip():
                            pages_without_text.append(
                                page_index + 1
                            )

                        for category, words in keywords.items():

                            for word in words:

                                pattern = (
                                    r"\b"
                                    + re.escape(word)
                                    + r"\b"
                                )

                                for match in re.finditer(
                                    pattern,
                                    text,
                                    re.IGNORECASE
                                ):

                                    start = max(
                                        0,
                                        match.start() - 100
                                    )

                                    end = min(
                                        len(text),
                                        match.end() + 100
                                    )

                                    context = text[
                                        start:end
                                    ].replace("\n", " ")

                                    results.append({
                                        "PDF Page": page_index + 1,
                                        "Category": category,
                                        "Keyword": match.group(),
                                        "Context": context,
                                        "Review Status": "Pending Review"
                                    })

                st.success("Screening completed!")

                st.metric("Pages Processed", total_pages)
                st.metric("Keyword Matches", len(results))

                if pages_without_text:
                    st.warning(
                        f"{len(pages_without_text)} pages "
                        "contained no extractable text. "
                        "These pages may require OCR."
                    )

                if results:

                    df = pd.DataFrame(results)

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    output = BytesIO()

                    with pd.ExcelWriter(
                        output,
                        engine="openpyxl"
                    ) as writer:

                        df.to_excel(
                            writer,
                            index=False,
                            sheet_name="Screening Results"
                        )

                    st.download_button(
                        label="Download Excel Report",
                        data=output.getvalue(),
                        file_name="BookGuard_UAE_Report.xlsx",
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        )
                    )

                else:
                    st.info(
                        "No predefined keywords were detected "
                        "in the extracted text. This does not "
                        "confirm that the book is suitable."
                    )

            except Exception as error:
                st.error(
                    "Unable to process this PDF. "
                    "Check whether it is valid, "
                    "encrypted, or password-protected."
                )

st.divider()

st.caption(
    "BookGuard UAE | Educational Resource Screening "
    "| Human Review Required"
)

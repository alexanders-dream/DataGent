def get_social_badges_html():
    """Returns HTML for ProductHunt and Google Form badges."""
    return """<div style="display: flex; flex-direction: row; gap: 20px; margin-top: 20px; text-align: center;">
        <div>
            <a href="https://www.producthunt.com/posts/datagent?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-datagent" target="_blank">
                <img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=909266&theme=light&t=1740388574757" alt="DataGent - Data&#0032;Analysis&#0032;made&#0032;easy&#0046;&#0032;A&#0032;Data&#0032;Analysis&#0032;AI&#0032;Agent | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" />
            </a>
            <p style="color: #33353d; font-weight: 600; margin-top: 5px;">Vote for DataGent!</p>
        </div>
        <div>
            <a href="https://docs.google.com/forms/d/e/1FAIpQLScZFxCR5jMSWUGU-WW1eSuQKuvjR6pI8YWvUIe85ozXGl9ysA/viewform?usp=header" target="_blank">
                <div style="background-color: #33353d; padding: 15px 30px; border-radius: 8px; text-align: center; width: 250px; height: 54px; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease;">
                    <span style="color: white; font-weight: 600; font-size: 16px;">📝 Share Feedback</span>
                </div>
            </a>
            <p style="color: #33353d; font-weight: 600; margin-top: 5px;">We value your input!</p>
        </div>
       </div>
    """

def get_calendly_badge_html():
    """Returns HTML for Calendly booking badge."""
    return """
        <div style="margin-left: 0px; margin-top: 20px;">
            <a href="https://calendly.com/alexanderoguso/30min" target="_blank">
                <div style="background-color:rgb(35, 135, 162); padding: 15px 30px; border-radius: 8px; text-align: center; width: 250px; height: 54px; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease;">
                    <span style="color: white; font-weight: 600; font-size: 16px;">📞 Need more? Book a call</span>
                </div>
            </a>
            <p style="color: #ffffff; font-weight: 600; margin-top: 5px; text-align: center;">Let's chat</p>
        </div>
    """

def get_buymeacoffee_badge_html():
    """Returns HTML for Buy Me A Coffee badge."""
    return """<div style="text-align: center; margin-top: 20px;">
            <a href="https://buymeacoffee.com/oguso">
                <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 150px; height: auto;">
            </a>
            <p style="color: #ffffff; margin-top: 5px;">Support my work!</p>
        </div>
    """

def get_button_css():
    """Returns CSS to style Streamlit buttons."""
    return """
    <style>div.stButton > button {padding: 0.25em 0.5em; font-size: 0.8em;}</style>
    <div style='margin-top: 0.5em;'>
    """

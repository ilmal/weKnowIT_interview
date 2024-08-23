import { Outlet, Link } from "react-router-dom";
import { useEffect, useState } from "react";

const Layout = () => {

    const [languages, setLanguages] = useState([])
    const [set_language, setSet_language] = useState("")

    useEffect(()=>{
        const URL = process.env.REACT_APP_BACKEND_URL + "/api/get_languages"
        const requestOptions = {
            method: 'GET',
        };
        fetch(URL, requestOptions)
            .then(response => response.json())
            .then(data => {
                setLanguages(data)
            })
        if (languages.length !== 0){
            setSet_language(languages[0])
        }

        console.log("set_language Layout: ", set_language)

    }, [])

    const display_languages = ()=>{
        const return_arr = []

        languages.forEach(language => {
            return_arr.push(
                <p onClick={()=>{
                    setSet_language(language)
                }} key={language}>{language}</p>
            )
        });

        return return_arr
    }

    const back_to_top = ()=>{
        window.scrollTo(0, 0)
    }

    return (
        <>
            <div className="header">
                <div className="languages">
                    {
                        languages.length === 0?
                        null:
                        display_languages()
                    }
                </div>
                <div className="pages">
                    <Link to="/">
                        <p>Home</p>
                    </Link>
                </div>
            </div>
            <Outlet context={[set_language]} />
            <div className="footer">
                <p onClick={back_to_top}>Back to top</p>
            </div>
        </>
    )

}

export default Layout
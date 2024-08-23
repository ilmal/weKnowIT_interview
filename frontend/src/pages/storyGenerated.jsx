import { useEffect, useState } from "react"
import { useOutletContext } from "react-router-dom";



const StoryGenerated = () => {
    const [set_language] = useOutletContext();

    const queryParameters = new URLSearchParams(window.location.search)
    const story = queryParameters.get("story")

    const [story_data, setStory_data] = useState("")
    const [errMessage, setErrMessage] = useState("")

    useEffect(()=>{
        if (story === null) return

        const URL = process.env.REACT_APP_BACKEND_URL + 
                    `/api/get_generated_text?story=${story.replace("%20", " ")}&language=${"zh-cn"}`
        const requestOptions = {
            method: 'GET',
        };
        fetch(URL, requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("STORY DATA: ", data)
                setStory_data(data)
            })
            .catch(err => {
                setErrMessage(err.toString())
            })
            
    },[])

    const display_text = ()=>{
        if (story_data.length === 0) return
        const return_arr = []
        let counter = 0

        for (let i=0; i<story_data.english_story.length; i++){
            return_arr.push(
                <div key={i}>
                    <p className="original_text hide_text" id={"original_text_" + i}>{story_data.english_story[i]}</p>
                    <p className="hide_text">test</p>
                    <p 
                    className="translated_text" id={"translated_text_" + i}>{story_data.pinyin_story[i].map((word, index) => {
                        return (
                            <span key={index} id={index} onTouchStart={(e)=>{
                                e.target.parentNode.previousElementSibling.classList.remove("hide_text")
                                e.target.parentNode.previousElementSibling.innerText = story_data.translation_array[i][e.target.id]
                                e.target.parentNode.previousElementSibling.previousElementSibling.classList.remove("hide_text")
                            }} 
                            onTouchEnd={(e)=>{
                                e.target.parentNode.previousElementSibling.classList.add("hide_text")
                                e.target.parentNode.previousElementSibling.previousElementSibling.classList.add("hide_text")
                            }}
                            >{word + " "}</span>
                        )
                    })}</p>
                </div>
            )
        }

        // story_data.forEach(story_segment => {
        //     counter += 1
        // });

        return return_arr
    }


    return (
        <div className="story">
            {
                (story_data) === ""?
                <div className="loading_message">
                    {
                        errMessage === ""?
                        null:
                        errMessage
                    }
                    <p className="loading_message_main">DATA IS LOADING! ;-;</p>
                    <p className="loading_message_inner">This may take a while :(</p>
                </div>
                :
                display_text()
            }
        </div>
    )

}

export default StoryGenerated

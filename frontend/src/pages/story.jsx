import { useEffect, useState } from "react"
import { useOutletContext } from "react-router-dom";



const Story = () => {
    const [set_language] = useOutletContext();

    const queryParameters = new URLSearchParams(window.location.search)
    const story = queryParameters.get("story")

    const [story_data, setStory_data] = useState("")
    const [errMessage, setErrMessage] = useState("")

    useEffect(()=>{
        if (story === null) return

        const URL = process.env.REACT_APP_BACKEND_URL + 
                    `/api/get_story_text?story=${story.replace("%20", " ")}&language=${"zh-cn"}`
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

        story_data.forEach(story_segment => {
            return_arr.push(
                <div key={counter}>
                    <p className="original_text hide_text" id={"original_text_" + counter}>{story_segment[0]}</p>
                    <p 
                    onTouchStart={(e)=>{
                        e.target.previousElementSibling.classList.remove("hide_text")
                    }} 
                    onTouchEnd={(e)=>{
                        e.target.previousElementSibling.classList.add("hide_text")
                    }}
                    className="translated_text" id={"translated_text_" + counter}>{story_segment[1]}</p>
                </div>
            )
            counter += 1
        });

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

export default Story

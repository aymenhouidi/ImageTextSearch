import { useState } from 'react';
import axios from 'axios';
import React from 'react';
import styled from "styled-components";
const Button = styled.button`
  background-color: #b59fdd;
  color: #ecf8f6;
  padding: 0.5rem;
  font-family: sans-serif;
  border-radius: 0.3rem;
  cursor: pointer;
  margin-top: 1rem;
  border-style: hidden;
`;

const Styles = styled.div`
  padding: 20px;

  h1 {
    border-bottom: 1px solid white;
    color: #3d3d3d;
    font-family: sans-serif;
    font-size: 20px;
    font-weight: 600;
    line-height: 24px;
    padding: 10px;
    text-align: center;
  }

  form {
    background: #ecf8f6;
    border: 1px solid #dedede;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin: 0 auto;
    max-width: 500px;
    padding: 30px 50px;
  }

  input {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
  }
  select {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
  }
  textarea {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
  }

  label {
    color: #3d3d3d;
    display: block;
    font-family: sans-serif;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 5px;
  }

  .submitBtn {
    background-color: #226d68;
    color: #ecf8f6;
    font-family: sans-serif;
    font-size: 14px;
    margin: 20px 0px;
    height: 40px;
    border-style: hidden;
    .custom-file-upload {
      border: 1px solid #ccc;
      display: inline-block;
      padding: 6px 12px;
      cursor: pointer;
    }
  }
`;

export function Form() {
    const [word, setWord] = useState("");
    const [hits, setHits] = useState([]); // Initialize hits as an empty array
    const [productImage, setProductImage] = useState();
    const [productImageBack, setProductImageBack] = useState("");
    const [mot, setMot] = useState("");
    const [productImageNameBack, setProductImageNameBack] = useState("");

    const handleChange = (event) => {
        event.preventDefault();
        try{
        const fileUploaded = event.target.files[0];
        setProductImageNameBack(fileUploaded.name);
        setProductImage(fileUploaded);
        setProductImageBack(URL.createObjectURL(fileUploaded));}
        catch{
        }

    };

    const hiddenFileInput = React.useRef(null)

    const handleClick = (event) => {
        event.preventDefault();

        hiddenFileInput.current?.click();
    };
    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent form submission

        const fromElastic = new FormData()
        fromElastic.append('image_path', `uploads\\${productImageNameBack}`)
        const formData = new FormData();

        formData.append('file', productImage);

        const textOnlySearch = new FormData()
        textOnlySearch.append('text', mot)

        if (productImageNameBack === "") {
            try {
                const res = await axios.post('http://localhost:8000/textsearch/', textOnlySearch, {

                })
                if (res != null) {

                    setHits(res.data)

                }



            } catch (error) {
                console.error('Error uploading image:', error);
            }

        }


        else if (mot === "") {
            try {
                const res = await axios.post('http://localhost:8000/upload/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                })
                if (res != null) {
                    const result = await axios.post('http://127.0.0.1:8000/imagesearch/', fromElastic, {
                    })
                    if (result != null) {
                        setHits(result.data)
                    }
                }
                // }).then(
                //     axios.post('http://localhost:8000/imagesearch/', { 'image_path': `uploads\\deployment.png`}, {
                //     }).then((response) => {
                //         console.log(response)
                //     }
                //     )

                // )


            } catch (error) {
                console.error('Error uploading image:', error);
            }

        } else {
            fromElastic.append('text', mot)
            try {
                const res = await axios.post('http://localhost:8000/upload/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                })
                if (res != null) {
                    const result = await axios.post('http://127.0.0.1:8000/imagetextsearch/', fromElastic, {
                    })
                    if (result != null) {
                        setHits(result.data)
                    }
                }
                // }).then(
                //     axios.post('http://localhost:8000/imagesearch/', { 'image_path': `uploads\\deployment.png`}, {
                //     }).then((response) => {
                //         console.log(response)
                //     }
                //     )

                // )

            } catch (error) {
                console.error('Error uploading image:', error);
            }

        }
    };;


    return (
        <main>
            <div class="container">
                <form onSubmit={handleSubmit}>
                    <h1>Content Based Search Engine</h1>



                    <Button onClick={handleClick}>Upload an image</Button>
                    <input
                        type="file"
                        ref={hiddenFileInput}
                        style={{ display: "none" }}
                        className="custom-file-upload"
                        name="upload"
                        onChange={handleChange}
                    />
                    <br></br>
                    <img src={productImageBack} style={{ width: '75%', margin: '0 auto' }} />
                    {productImageBack !== "" && (<Button name="button" type="submit" onClick={() => window.location.href = '/'} >
                        Reset
                    </Button>)}
                    <br></br>

                    <label>Type a word</label>

                    <input
                        type="text"
                        className="custom-file-upload"
                        name="mot"
                        value={mot}
                        onChange={(event) => { setMot(event.target.value) }
                        }
                        onKeyPress={(event) => {
                            if (event.key === 'Enter') {
                                event.preventDefault(); // Prevent the default form submission via Enter key
                                handleSubmit(event); // Call your submit handler
                            }
                        }}
                    />
                    <Button name="button" type="submit" onClick={handleSubmit} >
                        Submit
                    </Button>
                </form>

                {hits.length > 0 && (
                    <div >

                        <ul>
                            {hits.length > 0 && (
                                <div>
                                    <br></br>
                                    <h2>Search Results</h2>
                                    <ul className="image-list">
                                        {hits.map((hit, index) => (
                                            <li key={index} className="image-item">
                                                {/* Display the hit data, modify this part as needed */}
                                                <img
                                                    src={`${hit}`}
                                                    alt={`Image ${index}`}
                                                    className="image"
                                                />
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </ul>
                    </div>
                )}

            </div>

        </main>
    );
}
export default function CreateEvent(props) {
    return (
        <Styles>
            <Form props={props} />
        </Styles>
    );
}

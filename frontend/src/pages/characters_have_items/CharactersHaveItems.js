import TableView from '../../components/TableView/TableView';
import {headers, tableData} from '../../data/charactersItemsData';
import Button from '../../components/Button';
import { Link, useNavigate } from 'react-router-dom';
import ShowIfLoaded from '../../components/ShowIfLoaded';
import { DataNext } from '../../axios/crud.js';
import { useEffect, useState } from 'react';

function CharactersHaveItems() {
    const [post, setPost] = useState([[]]);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        DataNext("TranslationOutputs").then((response) => {
            setPost(response);
            setIsLoading(false);
        });
    }, []);

    return(
        <>
            <div id="content">
                <h1>Characters Have Items</h1>
                <ShowIfLoaded isLoading = {isLoading}>
                    <TableView headers={headers} listData={post} />
                    <Link to="/addCharactersHaveItems"><Button>Add Translation</Button></Link>
                    <Button  onClick={() => { navigate(-1) }}>Cancel</Button>
                </ShowIfLoaded>
            </div>
        </>
    )
}

export default CharactersHaveItems;
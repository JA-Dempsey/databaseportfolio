import TableView from '../../components/TableView/TableView';
import {headers, tableData} from '../../data/gameData';
import Button from '../../components/Button';
import { SearchBar } from '../../components/SearchBar';

import { Link, useNavigate } from 'react-router-dom';

function Games() {

    const navigate = useNavigate();
    
    return(
        <div id="content">
            <h1>Games</h1>
            <TableView headers={headers} listData={tableData} />
            <Link to="/addGame"><Button>Add Game</Button></Link>
            <Button onClick={() => navigate(-1)}>Cancel</Button>

            <SearchBar />
        </div>
    )
}

export default Games;
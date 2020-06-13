import React from "react";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import isEmpty from 'lodash/isEmpty'


function SideBar (props) {
    return (
        <div className={props.className}>
            {isEmpty(props.data) ? '' : 
                <List disablePadding dense>
                    {Object.entries(props.data).map(([key, val]) => {
                        return (
                        <div>
                            <ListItem key={val}>
                                <ListItemText style={{'overflowWrap': 'anywhere'}}>{key}: {val}</ListItemText>
                            </ListItem>
                            <Divider />
                        </div>
                        )
                    })}
                </List>}
        </div>
    );
}

export default SideBar;
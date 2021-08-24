// Author: Huveyscan Kamar
import './App.css';
import { useState, useEffect } from 'react'
import { Layout, Menu, Breadcrumb, Table } from 'antd';
import { SettingFilled, UserOutlined, LaptopOutlined, NotificationOutlined, ReloadOutlined } from '@ant-design/icons';
import logo from './themoviedb.svg'

const { SubMenu } = Menu;
const { Header, Content, Footer, Sider } = Layout;
const columns = [
  {
    title: '#',
    dataIndex: 'order',
    key: 'order',
  },
  {
    title: 'ID',
    dataIndex: 'ID',
    key: 'ID',
  },
  {
    title: 'Name',
    dataIndex: 'Name',
    key: 'Name',
  },
  {
    title: 'Gender',
    dataIndex: 'Gender',
    key: 'Gender',
    render(text) {
      if(text === "Male")
        var color = "magenta"
      else if(text === "Female")
        color = "blue"
      else
        color = "black"
      return {
        props: {
          style: { color: color }
        },
        children: <div>{text}</div>
      };
    }
  },
  {
    title: 'Known For',
    dataIndex: 'Known_For',
    key: 'Known_For',
  },
  {
    title: 'Popularity',
    dataIndex: 'Popularity',
    key: 'Popularity',
    render(text) {
      if(text >= 7.5)
        var color = "green"
      else if(text >= 5 && text < 7.5)
        color = "lime"
      else if(text >= 2.5 && text < 5)
        color = "olive"
      else
        color = "black"
      return {
        props: {
          style: { color: color }
        },
        children: <div>{text}</div>
      };
    }
  },
];

function App() {

  var count = 1

  let [genderChoice, setGenderChoice] = useState("None");
  const changeGenderChoice = (choice) => {
    setGenderChoice(choice);
  }

  let [knownForChoice, setKnownForChoice] = useState("None");
  const changeKnownForChoice = (choice) => {
    setKnownForChoice(choice);
  }

  let [popularityChoice, setPopularityChoice] = useState("None");
  const changePopularityChoice = (choice) => {
    setPopularityChoice(choice);
  }

  const [articles, setArticles] = useState([])
  useEffect(() => {
    fetch('http://127.0.0.1:5000/', {
      'method': 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(resp => resp.json())
      .then(resp => setArticles(resp))
      .catch(error => console.log(error))
  }, [])

  function create_datasource() {
    const dataSource = []
    articles.map(article => {
      var wanted_data = true
      if (article[2] === 1)
        var gender = "Female"
      else if (article[2] === 2)
        gender = "Male"
      else
        gender = "Unknown"

      if ((genderChoice !== "None" && genderChoice !== gender) || (knownForChoice !== "None" && knownForChoice !== article[3]))
        wanted_data = false
      else if (popularityChoice !== "None")
      {
        if( (popularityChoice === "Very" && article[4] < 7.5) || 
            (popularityChoice === "Popular" && (article[4] >= 7.5 || article[4] < 5)) || 
            (popularityChoice === "Less" && (article[4] >= 5 || article[4] < 2.5)) ||
            (popularityChoice === "Non" && (article[4] >=2.5)))
          wanted_data = false
      }

        if (wanted_data) {
          var data = {
            key: count,
            order: count++,
            ID: article[0],
            Name: article[1],
            Gender: gender,
            Known_For: article[3],
            Popularity: article[4],
          }
          dataSource.push(data)
        }
    })
    return dataSource
  }

  function reset_filters() {
    changeGenderChoice("None")
    changeKnownForChoice("None")
    changePopularityChoice("None")
  }

  return (
    <Layout>
      <Header className="header">
        <img src={logo} className="image" alt="logo" height="50px" />
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
        </Breadcrumb>
        <Layout style={{ padding: '24px 0' }}>
          <Sider width={200}>
            <Menu
              mode="inline"
              style={{ height: '100%' }}
            >
              <SubMenu key="sub1" icon={<UserOutlined />} title="Gender">
                <Menu.Item key="1" onClick={() => changeGenderChoice("Female")}>Female</Menu.Item>
                <Menu.Item key="2" onClick={() => changeGenderChoice("Male")}>Male</Menu.Item>
                <Menu.Item key="2" onClick={() => changeGenderChoice("Unknown")}>Unknown</Menu.Item>
                <Menu.Item key="3" onClick={() => changeGenderChoice("None")}>Reset Gender Choice</Menu.Item>
              </SubMenu>
              <SubMenu key="sub2" icon={<LaptopOutlined />} title="Known for">
                <Menu.Item key="4" onClick={() => changeKnownForChoice("Acting")}>Known for Acting</Menu.Item>
                <Menu.Item key="5" onClick={() => changeKnownForChoice("Directing")}>Known for Directing</Menu.Item>
                <Menu.Item key="6" onClick={() => changeKnownForChoice("Writing")}>Known for Writing</Menu.Item>
                <Menu.Item key="7" onClick={() => changeKnownForChoice("None")}>Reset Choice</Menu.Item>
              </SubMenu>
              <SubMenu key="sub3" icon={<NotificationOutlined />} title="Popularity">
                <Menu.Item key="9" onClick={() => changePopularityChoice("Very")}>Very Popular (7.5+)</Menu.Item>
                <Menu.Item key="10" onClick={() => changePopularityChoice("Popular")}>Popular (5 - 7.5)</Menu.Item>
                <Menu.Item key="11" onClick={() => changePopularityChoice("Less")}>Less Popular (2.5 - 5)</Menu.Item>
                <Menu.Item key="12" onClick={() => changePopularityChoice("Non")}>Non-Popular (0 - 2.5)</Menu.Item>
                <Menu.Item key="12" onClick={() => changePopularityChoice("None")}>Reset Popularity</Menu.Item>
              </SubMenu>
              <Menu.Item icon={<SettingFilled />} key="13" onClick={() => reset_filters()}>Reset Filters</Menu.Item>
            </Menu>
          </Sider>
          <Content style={{ padding: '0 24px', minHeight: 280 }}>
            <Table dataSource={create_datasource()} columns={columns} />
          </Content>
        </Layout>
      </Content>
      <Footer style={{ textAlign: 'center' }}>TheMovieDB API Testing Project ©2021 Created by Huveyscan Kamar</Footer>
    </Layout>
  );
}

export default App;
// Author: Huveyscan Kamar
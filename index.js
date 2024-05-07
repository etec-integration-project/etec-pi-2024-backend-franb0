import express from 'express';
import bodyParser from 'body-parser';
import { Sequelize, Model, DataTypes } from 'sequelize';
import { config } from 'dotenv';

const app = express();
const port = 3000;

config();
const database = process.env.DATABASE_NAME
console.log(database)
const username = process.env.DATABASE_USERNAME
console.log(username)
const password = process.env.DATABASE_PASSWORD
console.log(password)
const host = process.env.DATABASE_HOST
console.log(host)
const sequelize = new Sequelize(
    database,
    username,
    password,
    {
        dialect: 'mysql',
        host: host
    });

class User extends Model { }
User.init({
    name: DataTypes.STRING,
    email: DataTypes.STRING,
    password: DataTypes.STRING
}, { sequelize, modelName: 'user' });

sequelize.sync();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/users', async (req, res) => {
    const users = await User.findAll();
    res.json(users);
});

app.get('/users/:id', async (req, res) => {
    const user = await User.findByPk(req.params.id);
    res.json(user);
});

app.post('/users', async (req, res) => {
    const user = await User.create(req.body);
    res.json(user);
});

app.put('/users/:id', async (req, res) => {
    const user = await User.findByPk(req.params.id);
    if (user) {
        await user.update(req.body);
        res.json(user);
    } else {
        res.status(404).json({ message: 'User not found' });
    }
});

app.delete('/users/:id', async (req, res) => {
    const user = await User.findByPk(req.params.id);
    if (user) {
        await user.destroy();
        res.json({ message: 'User deleted' });
    } else {
        res.status(404).json({ message: 'User not found' });
    }
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});
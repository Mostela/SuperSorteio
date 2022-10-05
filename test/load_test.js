import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Counter, Rate } from 'k6/metrics';

export const options = {
  stages: [
      { duration: '5m', target: 100 },
      { duration: '2m', target: 90 },
      { duration: '7m', target: 70 },
      { duration: '2m', target: 100 },
      { duration: '8m', target: 100 },
      { duration: '5m', target: 0 },
  ],
  thresholds: {
      'http_req_duration': ['avg<4500'],
      'http_req_failed': ['rate < 0.15'],
  },
};

const BASE_URL = 'http://localhost';

const sortedNumber = () => {
    const list_number = []
    for (let i = 0; i < 6; i++) {
        list_number.push(Math.floor(Math.random() * 59) + 1)
    }
    return list_number
}

export default () => {
    const data_created = {
        Email: 'joao-mostela@hotmail.com',
        keyGame: '',
        guidUser: '',
        numberList: sortedNumber()
    }

    const created_user = http.post(`${BASE_URL}/singup`, JSON.stringify(data_created), {
        headers: {
            'Content-Type': 'application/json',
        },
    });
	sleep(10);

    check(created_user, {
        'status 201 - User': (resp) => resp.status === 201
    });

    if (created_user.status === 201){
        data_created.guidUser = created_user.json('GuidUser')
        data_created.keyGame = created_user.json('KeyGame')

        const created_game = http.post(`${BASE_URL}/game`, JSON.stringify(data_created), {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        check(created_game, {
            'status 201 - Game': (resp) => resp.status === 201
        });
	    check(created_game, {
		    'status 400 - Game': (resp) => resp.status === 400
	    });
    }

    sleep(2);
};

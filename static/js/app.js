class Request
{
	async get(url)
	{
		const response = await fetch(url);

		return await response.json();
	}

	async post(url, data, header)
	{
		const response = await fetch(url,{
				method: 'POST',
				headers: header,
				body: data,
			});

		return await response.json();
	}
}

class Todos
{
	addTodo(data)
	{
		let list = document.querySelector('.list-group');
		let inner = `
			<li class="list-group-item d-flex justify-content-between bg-light">
				<span class="align-middle p-1 float-left"><b>${data.title}:</b> ${data.description}</span>
				<div class="float-right">
					<button class="btn btn-sm btn-warning finish mr-2" value="${data.id}">Finish</button>
					<button class="btn btn-sm btn-danger delete" value="${data.id}">Delete</button>
				</div>
			</li>
		`;
		list.innerHTML+= inner;
	}
}


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


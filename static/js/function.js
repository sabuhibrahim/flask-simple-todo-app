async function postData(url = '', data = {}, header) {
    let body = JSON.stringify(data)
    let headers = header;
    const response = await fetch(url, { method: 'POST', credentials: 'include', headers, body});
    return await response.json();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function multiSelect(element){
    options = element.querySelectorAll('option');
    data = [];
    options.forEach((item)=>{
        if (item.selected) {
            data.push(item.value);
        }
    });
    return data;
}

async function updateAll(){
    await fetch('refresh/').then((res) => {
        return res.json();
    }).then((resp)=>{   
        const postlist = document.querySelectorAll('.postsStyle');
        if (resp.status === 'OK') {
            let data = setUpdateData(resp.data);
            if (postlist.length === resp.data.length){
                postlist.forEach((item, index)=>{
                    item.querySelector(".panel-heading").innerHTML = data[index].header;
                    item.querySelector(".media-list").innerHTML = data[index].comment;
                    item.querySelector(".addbtn").value = resp.data[index].id;
                });
            }else{
                postlist.forEach((item, index)=>{
                    item.querySelector(".panel-heading").innerHTML = data[data.length-postlist.length+index].header;
                    item.querySelector(".media-list").innerHTML = data[data.length-postlist.length+index].comment;
                    item.querySelector(".addbtn").value = resp.data[data.length-postlist.length+index].id;
                });
                let inner;
                for (let i = 0; i < data.length-postlist.length; i++) {
                   inner += setUpdateDataNew(resp.data[i]);                
                }
                postlist.innerHTML = inner + postlist.innerHTML;               
            }
        }
        window.setTimeout(updateAll, 10000);
    });
}

function setUpdateData(data){
    let elem = [];
    
    data.forEach((item)=>{
        let head = `
                <a href="${item.url}">${item.urlText}</a>
                <br> 
                <p class="ml-2">${item.title}
                    <span class="text-muted pull-right mr-3" style="float:right">
                        <small class="text-muted agoDate" >${timeAgo(new Date(item.date))}
                            <input type="hidden" value="${item.date}">
                        </small>
                    </span>
                <p>
                <p class="ml-2">Kategoriya: ${item.category}</p>
                <p class="ml-3 postSubcategory">
                    Subkategoriyaları: ${ JSON.parse(item.subcat).toString()} 
                </p> `;
        let comments = '';
        item.comments.forEach((com)=>{
            comments += `<li class="media">
                            <a href="#" class="pull-left" style="float:left">
                                <img src="/media/user_1.jpg" alt="" class="img-circle">
                            </a>
                            <div class="media-body">
                                <span class="text-muted pull-right mr-3" style="float:right">
                                    <small class="text-muted agoDate" >
                                        ${timeAgo(new Date(com.date))}
                                    </small>
                                </span>
                                <strong class="text-success ml-2">
                                <a href="${com.url}">${com.urlText}</a> 
                                </strong>
                                <p class="ml-3">
                                    ${com.content}
                                </p>
                            </div>
                        </li>`;
        });
        elem.push({
            header : head,
            comment : comments,
        });
    });
    return elem;
}

function setUpdateDataNew(data){
    let last = '';
    last += `
        <div class="col-md-6 col-md-offset-2 col-sm-12 postsStyle">
            <div class="comment-wrapper">
                <div class="panel panel-info">
                    <div class="panel-heading"> 
                        <a href="${data.url}">${data.urlText}</a>
                        <br> 
                        <p class="ml-2">${data.title}
                            <span class="text-muted pull-right mr-3" style="float:right">
                                <small class="text-muted agoDate" >${timeAgo(new Date(data.date))}
                                    <input type="hidden" value="${data.date}">
                                </small>
                            </span>
                        <p>
                        <p class="ml-2">Kategoriya: ${data.category}</p>
                        <p class="ml-3 postSubcategory">
                            Subkategoriyaları: ${JSON.parse(data.subcat).toString()} 
                        </p>    
                    </div>
                    <div class="panel-body">
                        <br>
                        <p class="ml-3">
                            ${data.content}
                        </p>
                        <br>
                        <div class="clearfix"></div>
                        <hr>
                        <ul class="media-list">`; 

    data.comments.forEach((com)=>{
        last += `<li class="media">
                    <a href="#" class="pull-left" style="float:left">
                        <img src="/media/user_1.jpg" alt="" class="img-circle">
                    </a>
                    <div class="media-body">
                        <span class="text-muted pull-right mr-3" style="float:right">
                            <small class="text-muted agoDate" >
                                ${timeAgo(new Date(com.date))}
                            </small>
                        </span>
                        <strong class="text-success ml-2">
                        <a href="${com.url}">${com.urlText}</a> 
                        </strong>
                        <p class="ml-3">
                            ${com.content}
                        </p>
                    </div>
                </li>`;
    });
    last += `</ul>
                    <br>
                </div>
                <br>
                <div class="panel-footer">
                    <div>
                        <textarea name="comment_content" cols="40" rows="2" class="form-control form-control-sm CommentForm" placeholder="Komment yazın" maxlength="1000" required="" id="id_comment_content"></textarea>
                        <br>
                        <button type="button" class="btn btn-info pull-right btn-sm addbtn" style="float:right" value="${data.id}">Əlavə et</button>
                    </div>
                    <br><br>
                </div>
            </div>
        </div>
    </div>`;
    return last;
}

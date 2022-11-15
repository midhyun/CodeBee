function category_change() {
    if (document.studyform.categoryselect.options[document.studyform.categoryselect.selectedIndex].value == '9') {
      document.studyform.categorie.type = "text"
      document.studyform.categorie.value = "";
      document.studyform.categorie.focus();
    } else {
      document.studyform.categorie.type = "hidden"
      document.studyform.categorie.value = document.studyform.categoryselect.options[document.studyform.categoryselect.selectedIndex].value;
    }
  }

function studytype_change() {
    if (document.studyform.studytypeselect.options[document.studyform.studytypeselect.selectedIndex].value == '9') {
        document.studyform.study_type.type = "text"
        document.studyform.study_type.value = "";
        document.studyform.study_type.focus();
    } else {
        document.studyform.study_type.type = "hidden"
        document.studyform.study_type.value = document.studyform.studytypeselect.options[document.studyform.studytypeselect.selectedIndex].value;
    }
    }

function locationtype_change(target) {
    var temp = document.getElementById('map_wrap')
    var btnonline = document.getElementById('button-addon2')
    var input = document.getElementById('id_addr')
    if (target.value == '0') {
        input.placeholder = '직접 입력하거나 지도를 클릭해 마커를 표시하세요.'
        btnonline.type = 'button'
        temp.classList.remove('hide')
    } else {
        // var temp2 = document.getElementById('map_wrap')
        // var btnonline2 = document.getElementById('button-addon2')
        // var input2 = document.getElementById('id_addr')
        input.placeholder = '온라인에서 활동할 주소를 입력해 주세요.'
        btnonline.type = 'hidden'
        temp.classList.add('hide')
    }
    }
var enteraddress = document.querySelector('[name="location"]')
enteraddress.addEventListener('keydown', function (event) {
    if (event.keyCode === 13) {
    document.getElementById('button-addon2').click();

    };
}, true);

// var mapContainer = document.getElementById('map'),
//     mapOption = {
//     center: new kakao.maps.LatLng(33.450701, 126.570667),
//     level: 3
//     };


// var geocoder = new kakao.maps.services.Geocoder();
// geocoder.addressSearch(`{{ location.location }}`, function (result, status) {
//     if (status === kakao.maps.services.Status.OK) {
//     var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
//     map.setCenter(coords);
//     }
// });

// var map = new kakao.maps.Map(mapContainer, mapOption);
// 마커를 담을 배열입니다
var markers = [];

var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption); 

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

// 키워드로 장소를 검색합니다
searchPlaces();

// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {

    var keyword = document.getElementById('id_addr').value;



    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch( keyword, placesSearchCB);

}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);
        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {
    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'click', function() {
                var markposition = marker.getPosition()
                document.studyform.X.value = markposition['La']
                document.studyform.Y.value = markposition['Ma']
                document.studyform.location.value = title
                displayInfowindow(marker, title);
            });

            itemEl.click =  function () {
                document.studyform.X.value = markposition['La']
                document.studyform.Y.value = markposition['Ma']
                document.studyform.location.value = title
                displayInfowindow(marker, title);
            };

        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
                 
      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';           

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage 
        });

    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}
var geocoder = new kakao.maps.services.Geocoder();

var marker_add = new kakao.maps.Marker({
    position: map.getCenter()
});
marker_add.setZIndex(3);
marker_add.setMap(map);

kakao.maps.event.addListener(map, 'click', function (mouseEvent) {
    function searchAddrFromCoords(coords, callback) {
    geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);
    }

    function searchDetailAddrFromCoords(coords, callback) {
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
    }
    searchDetailAddrFromCoords(mouseEvent.latLng, function (result, status) {
    if (status === kakao.maps.services.Status.OK) {
        var detailAddr = !!result[0].road_address ? '<div>도로명주소 : ' + result[0].road_address.address_name + '</div>' : '';
        detailAddr += '<div>지번 주소 : ' + result[0].address.address_name + '</div>';
        marker_add.setPosition(mouseEvent.latLng);
        marker_add.setMap(map);
        document.studyform.location.value = result[0].road_address.address_name

    }
    });

    var latlng = mouseEvent.latLng;

    // 마커 위치를 클릭한 위치로 옮깁니다
    marker_add.setPosition(latlng);
    document.studyform.X.value = latlng['La']
    document.studyform.Y.value = latlng['Ma']

});

var input = document.getElementById("id_tag")
new Tagify(input, {
        maxTags : 5
    })
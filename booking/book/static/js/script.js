function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
  
  window.onscroll = function () {
    scrollFunction();
  };
  
  function scrollFunction() {
    const scrollToTopBtn = document.getElementById("scrollToTopBtn");
    if (
      document.body.scrollTop > 200 ||
      document.documentElement.scrollTop > 200
    ) {
      scrollToTopBtn.style.display = "block";
    } else {
      scrollToTopBtn.style.display = "none";
    }
  }
  $(document).ready(function() {
    $("#category_autocomplete").autocomplete({
        source: function(request, response) {
            $.getJSON("{% url 'book:autocomplete' %}", {
                term: request.term
            }, response);
        },
        minLength: 2,
        select: function(event, ui) {
            event.preventDefault();
            $("#category_autocomplete option").each(function() {
                if ($(this).text() == ui.item.value) {
                    $(this).prop('selected', true);
                }
            });
        }
    }).autocomplete("instance")._renderItem = function(ul, item) {
        return $("<li>")
            .append("<div>" + item.value + "</div>")
            .appendTo(ul);
    };
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();

      document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
      });
  });
  });

  document.addEventListener('DOMContentLoaded', function () {
      let form = document.getElementById('newsletter_form');
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        let formData = new FormData(form);
        fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value,
          },
        })
          .then(function (response) {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error('Failed to subscribe. Please try again.');
            }
          })
          .then(function (data) {
            if (data.success) {
              alert('Successfully subscribed to the newsletter!');
            } else {
              console.log('Form errors:', data.errors);
              for (let field in data.errors) {
                console.log('Error in field:', field, '-', data.errors[field]);
              }
              alert('Failed to subscribe. Please try again.');
            }
          })
          .catch(function (error) {
            console.error('Error:', error);
            alert('Failed to subscribe. Please try again.');
          });
      });
    });
  
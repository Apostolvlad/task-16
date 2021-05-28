from re import template
import service_file
import service_write_html
import os
import shutil

def process_base_page(ignore_key = ('pageTitle', 'city', 'prepositional', 'metroId', 'districtId', 'SectionId', 'ContainerId', 'seoId')):
    base_page = service_file.cvs_convert_json('FAQ - FAQ.csv')
    for data_page in base_page:
        data_page['pageTitle'] = data_page['pageTitle'].lower()
        for key, value in data_page.items():
            if key in ignore_key: continue
            data_page[key] = value.format(**data_page).replace(' \\N', '').replace('\\N', '')
    return base_page

def process_html(base_page):
    try: 
        os.mkdir('result')
    except OSError:
        shutil.rmtree('result')
        os.mkdir('result')
    sh = "update SeoData set questions='{0}' where id={1};"
    template = service_write_html.get_template()
    base_result = list()
    for data_page in base_page:
        index = service_write_html.fill_html(data_page, template['page'], '')
        with open(f'result\\{data_page["pageTitle"]}.html', 'w', encoding='utf-8') as f:
            f.write(index)
        base_result.append(sh.format(index, data_page['seoId']))
    with open(f'result.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(base_result))

def main():
    base_page = process_base_page()
    process_html(base_page)
    print()
    

    

if __name__ == '__main__':
    main()
    
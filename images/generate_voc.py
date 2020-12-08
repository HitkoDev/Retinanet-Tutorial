
import os
import shutil

import cv2
from glob import glob


def main():
    awe_dir = 'AWEForSegmentation'
    save_dir = 'AWE'
    annot_dir = os.path.join(save_dir, 'Annotations')
    sets_dir = os.path.join(save_dir, 'ImageSets', 'Main')
    img_dir = os.path.join(save_dir, 'JPEGImages')

    if not os.path.exists(annot_dir):
        os.makedirs(annot_dir)
    if not os.path.exists(sets_dir):
        os.makedirs(sets_dir)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    train_file = open(os.path.join(sets_dir, 'train.txt'), 'w+')
    val_file = open(os.path.join(sets_dir, 'val.txt'), 'w+')
    all_file = open(os.path.join(sets_dir, 'trainval.txt'), 'w+')

    i = 0
    for folder in ['train', 'test']:
        src_dir = os.path.join(awe_dir, folder)
        annot = os.path.join(awe_dir, '{}annot_rect'.format(folder))
        images = glob('{}/**/*'.format(src_dir), recursive=True)
        images = [i for i in images if os.path.exists(
            i.replace(src_dir, annot))]

        for path in images:
            dest = str(i)
            dest_file = dest + '.png'
            dest_path = os.path.join(img_dir, dest_file)
            i += 1

            all_file.write(dest + '\n')
            if folder == 'train':
                train_file.write(dest + '\n')
            else:
                val_file.write(dest + '\n')

            shutil.copy2(path, dest_path)
            mask = cv2.imread(path.replace(src_dir, annot))
            w, h, ch = mask.shape
            gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
            contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            data = ["""<annotation>
	<folder>JPEGImages</folder>
	<filename>{}</filename>
	<path>{}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>{}</width>
		<height>{}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>""".format(dest_file, dest_path, w, h)]
            for c in contours:
                x1 = min([p[0][0] for p in c if p[0][0] >= 0]) + 1
                x2 = max([p[0][0] for p in c if p[0][0] >= 0]) + 1
                y1 = min([p[0][1] for p in c if p[0][1] >= 0]) + 1
                y2 = max([p[0][1] for p in c if p[0][1] >= 0]) + 1
                data.append("""	<object>
		<name>ear</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>""".format(x1, y1, x2, y2))
            data.append("""</annotation>""")
            with open(os.path.join(annot_dir, dest + '.xml'), 'w+') as f:
                f.write('\n'.join(data))

    train_file.close()
    val_file.close()
    all_file.close()


if __name__ == '__main__':
    main()
